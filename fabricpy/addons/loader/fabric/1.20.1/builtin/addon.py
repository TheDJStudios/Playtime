ADDON_KIND = "loader"
ADDON_TARGET = "fabric"
MINECRAFT_VERSION = "1.20.1"
ADDON_NAME = "builtin"
ADDON_PRIORITY = -100


def generate_project(mod, project_dir):
    from fabricpy.compiler.fabric_gen import generate_fabric_project

    return generate_fabric_project(mod, project_dir)
