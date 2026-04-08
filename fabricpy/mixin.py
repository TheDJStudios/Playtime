"""
Mixin base class. Subclass this to inject into existing Minecraft/Fabric classes.

Mixins are the most powerful (and dangerous) modding tool — they let you hook
directly into Minecraft's internals and change behaviour at the bytecode level.

Example:
    class PlayerTeleportMixin(mc.Mixin):
        target_class = "net.minecraft.server.network.ServerPlayerEntity"

        @mc.inject(method="teleport", at="HEAD", cancellable=True)
        def on_teleport(self, ctx):
            ctx.player.send_message("Teleporting!")

Class attributes:
    target_class    str     Fully qualified Java class to inject into  (required)
    priority        int     Mixin priority (default: 1000)
"""


class MixinMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        injections = {}
        for attr_name, val in namespace.items():
            if callable(val) and hasattr(val, "_fabricpy_hook") and val._fabricpy_hook == "inject":
                injections[attr_name] = val
        cls._injections = injections
        return cls


class Mixin(metaclass=MixinMeta):
    target_class: str = ""
    priority: int = 1000

    _injections: dict = {}

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__ + "Mixin"

    @classmethod
    def get_injections(cls) -> dict:
        return cls._injections
