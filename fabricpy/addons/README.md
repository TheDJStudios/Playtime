Addon root for `fabricpy`.

Folder layout:

- `fabricpy/addons/loader/<loader>/<minecraft_version>/<addon_name>/addon.py`

Example:

- `fabricpy/addons/loader/fabric/1.20.1/builtin/addon.py`
- `fabricpy/addons/loader/quilt/1.20.1/my_quilt_loader/addon.py`

Required module attributes in `addon.py`:

- `ADDON_KIND = "loader"`
- `ADDON_TARGET = "<loader name>"`
- `MINECRAFT_VERSION = "<mc version>"`
- `ADDON_NAME = "<addon name>"`

Optional:

- `ADDON_PRIORITY = 0`

Required functions:

- `generate_project(mod, project_dir)`

Optional:

- `build_project(project_dir, minecraft_version, clean=False, output_dir=None)`

If `build_project(...)` is omitted, `fabricpy` falls back to the default Gradle runner.
