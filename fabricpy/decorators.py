"""
Decorators that mark Python methods as Minecraft event hooks.
These get picked up by the compiler and translated to Java override methods.
"""

def _mark(hook_type, **kwargs):
    """Internal: mark a function with a hook type."""
    def decorator(func):
        func._fabricpy_hook = hook_type
        func._fabricpy_hook_args = kwargs
        return func
    return decorator


def on_use(func):
    """
    Block: Called when a player right-clicks the block.
    Maps to: onUse() / use() override.

    Java params available via ctx:
        ctx.player, ctx.world, ctx.pos, ctx.state, ctx.hand
    """
    func._fabricpy_hook = "on_use"
    func._fabricpy_hook_args = {}
    return func


def on_right_click(func):
    """
    Item: Called when a player right-clicks with the item.
    Maps to: use() override.

    Java params available via ctx:
        ctx.player, ctx.world, ctx.stack, ctx.hand
    """
    func._fabricpy_hook = "on_right_click"
    func._fabricpy_hook_args = {}
    return func


def on_hold(func):
    """
    Item: Called every tick while a player is actively holding the item.
    This includes the selected main hand slot and the offhand.

    Java params available via ctx:
        ctx.player, ctx.world, ctx.stack, ctx.hand
    """
    func._fabricpy_hook = "on_hold"
    func._fabricpy_hook_args = {}
    return func


def on_place(func):
    """
    Block: Called when the block is placed.
    Maps to: onPlaced() override.

    Java params available via ctx:
        ctx.player, ctx.world, ctx.pos, ctx.state
    """
    func._fabricpy_hook = "on_place"
    func._fabricpy_hook_args = {}
    return func


def on_break(func):
    """
    Block: Called when the block is broken.
    Maps to: onBreak() override.

    Java params available via ctx:
        ctx.player, ctx.world, ctx.pos, ctx.state
    """
    func._fabricpy_hook = "on_break"
    func._fabricpy_hook_args = {}
    return func


def on_tick(func):
    """
    Block: Called every game tick while the block exists (requires BlockEntity).
    Maps to: tick() on the block entity.

    Java params available via ctx:
        ctx.world, ctx.pos, ctx.state
    """
    func._fabricpy_hook = "on_tick"
    func._fabricpy_hook_args = {}
    return func


def inject(method: str, at: str = "HEAD", cancellable: bool = False):
    """
    Mixin injection decorator.

    Args:
        method: Target method signature, e.g. "teleport(DDD)V"
        at: Injection point — "HEAD", "TAIL", or "INVOKE:..."
        cancellable: Whether to allow cancelling the original method via ci.cancel()

    Example:
        @mc.inject(method="teleport", at="HEAD", cancellable=True)
        def on_teleport(self, ctx):
            ctx.player.send_message("Teleporting!")
    """
    return _mark("inject", method=method, at=at, cancellable=cancellable)
