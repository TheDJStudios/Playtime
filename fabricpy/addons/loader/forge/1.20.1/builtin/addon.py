ADDON_KIND = "loader"
ADDON_TARGET = "forge"
MINECRAFT_VERSION = "1.20.1"
ADDON_NAME = "builtin"
ADDON_PRIORITY = -100


def generate_project(mod, project_dir):
    from fabricpy.compiler.forge_gen import generate_forge_project

    return generate_forge_project(mod, project_dir)
