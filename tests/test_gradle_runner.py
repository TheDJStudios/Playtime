from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, mock
import stat

from fabricpy.compiler import gradle_runner


class GradleRunnerPortabilityTests(TestCase):
    def test_manual_wrapper_command_is_os_specific(self):
        project_dir = Path("/tmp/example-project")

        with mock.patch.object(gradle_runner.sys, "platform", "win32"):
            self.assertEqual(
                gradle_runner._manual_gradle_wrapper_command(project_dir, "8.8"),
                'cd /d "/tmp/example-project" && gradle wrapper --gradle-version 8.8 && gradlew.bat build',
            )

        with mock.patch.object(gradle_runner.sys, "platform", "darwin"):
            self.assertEqual(
                gradle_runner._manual_gradle_wrapper_command(project_dir, "8.8"),
                'cd "/tmp/example-project" && gradle wrapper --gradle-version 8.8 && ./gradlew build',
            )

    def test_gradle_command_uses_cmd_on_windows(self):
        project_dir = Path("/tmp/example-project")

        with mock.patch.object(gradle_runner.sys, "platform", "win32"):
            self.assertEqual(
                gradle_runner._gradle_command(project_dir, "--no-daemon", "build"),
                ["cmd.exe", "/d", "/c", str(project_dir / "gradlew.bat"), "--no-daemon", "build"],
            )

    def test_gradle_command_uses_shell_script_on_unix(self):
        project_dir = Path("/tmp/example-project")

        with mock.patch.object(gradle_runner.sys, "platform", "linux"):
            self.assertEqual(
                gradle_runner._gradle_command(project_dir, "--no-daemon", "build"),
                [str(project_dir / "gradlew"), "--no-daemon", "build"],
            )

    def test_written_unix_wrapper_avoids_readlink_f(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)

            with mock.patch.object(gradle_runner.sys, "platform", "darwin"):
                gradle_runner._write_wrapper_scripts(project_dir, "8.8")

            unix_wrapper = (project_dir / "gradlew").read_text(encoding="utf-8")
            self.assertIn('APP_HOME=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)', unix_wrapper)
            self.assertNotIn("readlink -f", unix_wrapper)

    def test_ensure_wrapper_executable_repairs_existing_unix_wrapper(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            wrapper = project_dir / "gradlew"
            wrapper.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            wrapper.chmod(0o644)

            with mock.patch.object(gradle_runner.sys, "platform", "darwin"):
                gradle_runner._ensure_wrapper_executable(project_dir)

            mode = stat.S_IMODE(wrapper.stat().st_mode)
            self.assertEqual(mode, 0o755)

    def test_wrapper_script_needs_refresh_for_stale_macos_script(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            wrapper_dir = project_dir / "gradle" / "wrapper"
            wrapper_dir.mkdir(parents=True, exist_ok=True)
            (project_dir / "gradlew").write_text(
                '#!/bin/sh\nAPP_HOME=$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")\n',
                encoding="utf-8",
            )
            (wrapper_dir / "gradle-wrapper.properties").write_text(
                "distributionUrl=https\\://services.gradle.org/distributions/gradle-8.8-bin.zip\n",
                encoding="utf-8",
            )

            with mock.patch.object(gradle_runner.sys, "platform", "darwin"):
                self.assertTrue(gradle_runner._wrapper_script_needs_refresh(project_dir, "8.8"))

    def test_build_env_can_be_extended_with_project_local_gradle_home(self):
        env = gradle_runner._build_env(None)
        self.assertNotIn("GRADLE_USER_HOME", env)

        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            gradle_home = project_dir / ".gradle-user-home"
            gradle_home.mkdir(parents=True, exist_ok=True)
            env["GRADLE_USER_HOME"] = str(gradle_home)
            self.assertEqual(env["GRADLE_USER_HOME"], str(gradle_home))

    def test_wrapper_ready_requires_wrapper_jar(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            wrapper_dir = project_dir / "gradle" / "wrapper"
            wrapper_dir.mkdir(parents=True, exist_ok=True)
            (project_dir / "gradlew").write_text("#!/bin/sh\n", encoding="utf-8")
            (wrapper_dir / "gradle-wrapper.properties").write_text(
                "distributionUrl=https\\://services.gradle.org/distributions/gradle-8.8-bin.zip\n",
                encoding="utf-8",
            )

            self.assertFalse(gradle_runner._wrapper_ready(project_dir, "8.8"))

            (wrapper_dir / "gradle-wrapper.jar").write_text("jar", encoding="utf-8")
            self.assertTrue(gradle_runner._wrapper_ready(project_dir, "8.8"))

    def test_gradle_command_uses_absolute_project_path(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            relative_project = root / "nested" / "proj"
            relative_project.mkdir(parents=True, exist_ok=True)

            with mock.patch.object(gradle_runner.sys, "platform", "linux"):
                command = gradle_runner._gradle_command(relative_project.resolve(), "--no-daemon", "build")

            self.assertEqual(command[0], str(relative_project.resolve() / "gradlew"))
