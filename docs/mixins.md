# Mixins

Create a mixin by subclassing `mc.Mixin` and using `@mc.inject(...)`.

```python
@mod.register
class TeleportMonitor(mc.Mixin):
    target_class = "net.minecraft.server.network.ServerPlayerEntity"

    @mc.inject(method="teleport", at="HEAD", cancellable=True)
    def on_teleport(self, ctx):
        pass
```

Mixin fields:

- `target_class`: fully qualified Java class name
- `priority`: default `1000`

Injection decorator arguments:

- `method`
- `at`
- `cancellable`

Notes:

- mixins are the lowest-level part of the API
- use them when block, item, event, or command hooks are not enough
