"""
Gradle runner - sets up the Gradle wrapper and runs the build.

Requirements:
  - Java 17+ for Minecraft 1.20.1
  - Java 21+ for Minecraft 1.21.1
  - Gradle must be installed for first-time wrapper setup,
    OR the wrapper jar can be copied from another project.

After setup, ./gradlew handles everything automatically.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_GRADLE_VERSION = "8.8"


def _parse_version_tuple(version: str) -> tuple[int, ...]:
    parts = []
    for piece in re.findall(r"\d+", version):
        parts.append(int(piece))
    return tuple(parts)


def _gradle_version(gradle_bin: str, env: dict[str, str]) -> tuple[int, ...] | None:
    try:
        result = subprocess.run(
            [gradle_bin, "-v"],
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

    output = f"{result.stdout}\n{result.stderr}"
    match = re.search(r"Gradle\s+([0-9.]+)", output)
    if not match:
        return None
    return _parse_version_tuple(match.group(1))


def _wrapper_script_name() -> str:
    return "gradlew.bat" if sys.platform == "win32" else "gradlew"


def _manual_gradle_wrapper_command(project_dir: Path, gradle_version: str) -> str:
    project = str(project_dir)
    if sys.platform == "win32":
        return f'cd /d "{project}" && gradle wrapper --gradle-version {gradle_version} && gradlew.bat build'
    return f'cd "{project}" && gradle wrapper --gradle-version {gradle_version} && ./gradlew build'


def _gradle_command(project_dir: Path, *args: str) -> list[str]:
    wrapper_path = str(project_dir / _wrapper_script_name())
    if sys.platform == "win32":
        return ["cmd.exe", "/d", "/c", wrapper_path, *args]
    return [wrapper_path, *args]


def _ensure_wrapper_executable(project_dir: Path) -> None:
    if sys.platform == "win32":
        return
    wrapper_path = project_dir / "gradlew"
    if not wrapper_path.exists():
        return
    current_mode = wrapper_path.stat().st_mode
    wrapper_path.chmod(current_mode | 0o111)


def _wrapper_script_needs_refresh(project_dir: Path, gradle_version: str) -> bool:
    wrapper_script = project_dir / _wrapper_script_name()
    wrapper_props = project_dir / "gradle" / "wrapper" / "gradle-wrapper.properties"
    if not wrapper_script.exists() or not wrapper_props.exists():
        return True

    props_text = wrapper_props.read_text(encoding="utf-8", errors="ignore")
    if f"gradle-{gradle_version}-bin.zip" not in props_text:
        return True

    script_text = wrapper_script.read_text(encoding="utf-8", errors="ignore")
    if sys.platform != "win32" and "readlink -f" in script_text:
        return True
    return False


def _wrapper_jar_path(project_dir: Path) -> Path:
    return project_dir / "gradle" / "wrapper" / "gradle-wrapper.jar"


def _wrapper_ready(project_dir: Path, gradle_version: str) -> bool:
    wrapper_script = project_dir / _wrapper_script_name()
    wrapper_props = project_dir / "gradle" / "wrapper" / "gradle-wrapper.properties"
    wrapper_jar = _wrapper_jar_path(project_dir)
    if not wrapper_script.exists() or not wrapper_props.exists() or not wrapper_jar.exists():
        return False
    props_text = wrapper_props.read_text(encoding="utf-8", errors="ignore")
    return f"gradle-{gradle_version}-bin.zip" in props_text


def _find_wrapper_jar_candidates(project_dir: Path) -> list[Path]:
    candidates: list[Path] = []
    seen: set[str] = set()
    search_roots = [project_dir.parent, Path.home()]
    for root in search_roots:
        if not root.exists():
            continue
        for candidate in root.rglob("gradle-wrapper.jar"):
            resolved = str(candidate.resolve())
            if resolved in seen:
                continue
            seen.add(resolved)
            candidates.append(candidate)
    return candidates

def _required_java_major(minecraft_version: str) -> int:
    version_map = {
        "1.20.1": 17,
        "1.21.1": 21,
    }
    return version_map.get(minecraft_version, 17)


def _required_gradle_version(loader: str, minecraft_version: str) -> str:
    if loader == "forge" and minecraft_version == "1.21.1":
        return "9.3.0"
    return DEFAULT_GRADLE_VERSION


def _java_major_version(java_exe: Path) -> int | None:
    try:
        result = subprocess.run(
            [str(java_exe), "-version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

    output = (result.stderr or result.stdout).strip()
    match = re.search(r'version "(\d+)', output)
    if not match:
        return None
    return int(match.group(1))


def _iter_java_candidates() -> list[Path]:
    candidates: list[Path] = []

    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        candidates.append(Path(java_home) / "bin" / ("java.exe" if sys.platform == "win32" else "java"))

    for env_name, env_value in os.environ.items():
        if env_name.upper().startswith("JDK") and env_name.upper().endswith("_HOME") and env_value:
            candidates.append(Path(env_value) / "bin" / ("java.exe" if sys.platform == "win32" else "java"))

    if sys.platform == "win32":
        program_files = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
        common_roots = [
            program_files / "Java",
            program_files / "Microsoft",
            program_files / "Eclipse Adoptium",
            program_files / "Zulu",
            program_files / "Amazon Corretto",
        ]
        for root in common_roots:
            if not root.exists():
                continue
            for candidate in sorted(root.rglob("java.exe"), reverse=True):
                candidates.append(candidate)

    which_java = shutil.which("java")
    if which_java:
        candidates.append(Path(which_java))

    path_parts = os.environ.get("PATH", "").split(os.pathsep)
    for part in path_parts:
        if not part:
            continue
        java_candidate = Path(part) / ("java.exe" if sys.platform == "win32" else "java")
        candidates.append(java_candidate)

    return candidates


def _find_java_executable(required_major: int) -> str | None:
    """Find a Java executable matching the required major version."""
    candidates = _iter_java_candidates()

    seen: set[str] = set()
    exact_matches: list[tuple[int, str]] = []
    fallback_matches: list[tuple[int, str]] = []

    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except FileNotFoundError:
            continue
        if str(resolved) in seen or not resolved.exists():
            continue
        seen.add(str(resolved))

        major = _java_major_version(resolved)
        if major is None:
            continue
        if major == required_major:
            exact_matches.append((major, str(resolved)))
        elif major > required_major:
            fallback_matches.append((major, str(resolved)))

    if exact_matches:
        return exact_matches[0][1]
    if fallback_matches:
        fallback_matches.sort(key=lambda item: item[0])
        return fallback_matches[0][1]

    return None


def _build_env(java_exe: str | None = None) -> dict[str, str]:
    """Build an environment that prefers the selected Java executable."""
    env = os.environ.copy()
    if not java_exe:
        return env

    java_bin = str(Path(java_exe).parent)
    java_home = str(Path(java_exe).parent.parent)
    path_parts = [java_bin] + [
        part for part in env.get("PATH", "").split(os.pathsep)
        if part and part != java_bin
    ]
    env["JAVA_HOME"] = java_home
    env["PATH"] = os.pathsep.join(path_parts)
    return env


def _check_java(minecraft_version: str) -> str | None:
    """Verify the required Java version is available and return its executable path."""
    required_major = _required_java_major(minecraft_version)
    java_exe = _find_java_executable(required_major)
    if java_exe:
        return java_exe

    which_java = shutil.which("java")
    if which_java:
        try:
            result = subprocess.run(
                [which_java, "-version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = (result.stderr or result.stdout).strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            output = ""
        if output:
            print(f"[fabricpy] Warning: Java {required_major}+ required for Minecraft {minecraft_version}. Found: {output[:120]}")
        else:
            print(f"[fabricpy] Warning: Java {required_major}+ required for Minecraft {minecraft_version}, but the detected 'java' could not be used.")
        return None

    print(
        f"[fabricpy] Error: Java {required_major}+ not found for Minecraft {minecraft_version}. "
        "Install a matching JDK or set JAVA_HOME/JDK*_HOME."
    )
    return None


def _setup_gradle_wrapper(project_dir: Path, env: dict[str, str], gradle_version: str) -> bool:
    """
    Set up the Gradle wrapper in project_dir.

    Strategy:
    1. If `gradle` is on PATH, run `gradle wrapper --gradle-version <required>`
    2. Otherwise, try to copy wrapper from another project.
    """
    wrapper_script = project_dir / _wrapper_script_name()
    wrapper_props = project_dir / "gradle" / "wrapper" / "gradle-wrapper.properties"

    if wrapper_script.exists() and wrapper_props.exists():
        if _wrapper_script_needs_refresh(project_dir, gradle_version):
            print(f"[fabricpy] Refreshing Gradle wrapper scripts for {gradle_version}...")
            _write_wrapper_scripts(project_dir, gradle_version)
        _ensure_wrapper_executable(project_dir)
        if _wrapper_ready(project_dir, gradle_version):
            print("[fabricpy] Gradle wrapper already present.")
            return True
        print(f"[fabricpy] Updating/incompletely repairing Gradle wrapper to {gradle_version}...")
    elif wrapper_script.exists():
        print("[fabricpy] Wrapper scripts exist but wrapper metadata is incomplete; rebuilding them.")

    gradle_bin = shutil.which("gradle", path=env.get("PATH"))
    if gradle_bin:
        detected_version = _gradle_version(gradle_bin, env)
        required_version = _parse_version_tuple(gradle_version)
        if detected_version is not None and detected_version >= required_version:
            print("[fabricpy] Setting up Gradle wrapper via system Gradle...")
            result = subprocess.run(
                [gradle_bin, "wrapper", "--gradle-version", gradle_version],
                cwd=project_dir,
                capture_output=True,
                text=True,
                env=env,
            )
            if result.returncode == 0:
                print("[fabricpy] Gradle wrapper ready.")
                return True
            print(f"[fabricpy] gradle wrapper failed:\n{result.stderr}")
        else:
            print(
                f"[fabricpy] Skipping system Gradle bootstrap because it is too old for wrapper {gradle_version}."
            )

    print("[fabricpy] Generating minimal Gradle wrapper scripts...")
    _write_wrapper_scripts(project_dir, gradle_version)

    jar_path = _wrapper_jar_path(project_dir)
    jar_path.parent.mkdir(parents=True, exist_ok=True)

    jar_candidates = _find_wrapper_jar_candidates(project_dir)
    if jar_candidates:
        shutil.copy2(jar_candidates[0], jar_path)
        print(f"[fabricpy] Copied gradle-wrapper.jar from {jar_candidates[0]}")
        return True

    print("[fabricpy] Could not find gradle-wrapper.jar.")
    print("[fabricpy] Please install Gradle (https://gradle.org/install/) and run:")
    print(f"    {_manual_gradle_wrapper_command(project_dir, gradle_version)}")
    return False


def _write_wrapper_scripts(project_dir: Path, gradle_version: str):
    """Write gradlew and gradlew.bat scripts."""
    wrapper_dir = project_dir / "gradle" / "wrapper"
    wrapper_dir.mkdir(parents=True, exist_ok=True)

    (wrapper_dir / "gradle-wrapper.properties").write_text(
        "distributionBase=GRADLE_USER_HOME\n"
        "distributionPath=wrapper/dists\n"
        f"distributionUrl=https\\://services.gradle.org/distributions/gradle-{gradle_version}-bin.zip\n"
        "networkTimeout=10000\n"
        "validateDistributionUrl=true\n"
        "zipStoreBase=GRADLE_USER_HOME\n"
        "zipStorePath=wrapper/dists\n"
    , encoding="utf-8")

    gradlew = r"""#!/bin/sh
##############################################################################
# Gradle start up script for UN*X
# Generated by fabricpy
##############################################################################
APP_HOME=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
if [ -n "$JAVA_HOME" ]; then
  exec "$JAVA_HOME/bin/java" -jar "$APP_HOME/gradle/wrapper/gradle-wrapper.jar" "$@"
fi
exec java -jar "$APP_HOME/gradle/wrapper/gradle-wrapper.jar" "$@"
"""
    gradlew_path = project_dir / "gradlew"
    gradlew_path.write_text(gradlew, encoding="utf-8")
    if sys.platform != "win32":
        gradlew_path.chmod(0o755)

    (project_dir / "gradlew.bat").write_text(
        "@rem Generated by fabricpy\r\n"
        "@echo off\r\n"
        "if defined JAVA_HOME (\r\n"
        "  \"%JAVA_HOME%\\bin\\java.exe\" -jar \"%~dp0gradle\\wrapper\\gradle-wrapper.jar\" %*\r\n"
        ") else (\r\n"
        "  java -jar \"%~dp0gradle\\wrapper\\gradle-wrapper.jar\" %*\r\n"
        ")\r\n",
        encoding="utf-8",
    )


def run_build(project_dir: Path, minecraft_version: str, loader: str, clean: bool = False, output_dir: Path = None) -> bool:
    """
    Run the Gradle build in project_dir and copy output .jar to output_dir.

    Returns True if build succeeded.
    """
    project_dir = project_dir.resolve()
    java_exe = _check_java(minecraft_version)
    if not java_exe:
        return False

    env = _build_env(java_exe)
    gradle_user_home = project_dir / ".gradle-user-home"
    gradle_user_home.mkdir(parents=True, exist_ok=True)
    env["GRADLE_USER_HOME"] = str(gradle_user_home)
    gradle_version = _required_gradle_version(loader, minecraft_version)

    if not _setup_gradle_wrapper(project_dir, env, gradle_version):
        print("[fabricpy] Build skipped - Gradle wrapper not set up.")
        print(f"[fabricpy] Source was generated at: {project_dir}")
        print("[fabricpy] Once you have Gradle installed, run:")
        print(f"    {_manual_gradle_wrapper_command(project_dir, gradle_version)}")
        return False

    _ensure_wrapper_executable(project_dir)
    task = "clean build" if clean else "build"
    cmd = _gradle_command(project_dir, "--no-daemon", *task.split())

    print(f"[fabricpy] Running: {' '.join(cmd)}")
    print("[fabricpy] (This will download Minecraft and Fabric/Forge on first run - may take a few minutes)")

    try:
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            timeout=600,
            env=env,
        )
    except subprocess.TimeoutExpired:
        print("[fabricpy] Build timed out after 10 minutes.")
        return False
    except KeyboardInterrupt:
        print("\n[fabricpy] Build cancelled.")
        return False

    if result.returncode != 0:
        print(f"[fabricpy] Build FAILED (exit code {result.returncode})")
        print("[fabricpy] Check the output above for Java compiler errors.")
        print(f"[fabricpy] Generated source is at: {project_dir / 'src'}")
        return False

    libs_dir = project_dir / "build" / "libs"
    if output_dir and libs_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        jars = [f for f in libs_dir.glob("*.jar") if "sources" not in f.name]
        for jar in jars:
            dest = output_dir / jar.name
            shutil.copy2(jar, dest)
            print(f"[fabricpy] Built: {dest}")

    return True
