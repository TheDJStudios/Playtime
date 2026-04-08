# Runtime Helpers

`fabricpy` now includes a broader runtime helper layer for math, raycasts, and particles.

## Math Helpers

Available helpers:

- `ctx.math.vec3(x, y, z)`
- `ctx.math.block_pos(x, y, z)`
- `ctx.math.clamp(value, min, max)`
- `ctx.math.lerp(start, end, delta)`
- `ctx.math.distance3(x1, y1, z1, x2, y2, z2)`
- `ctx.math.length3(x, y, z)`
- `ctx.math.normalize3(x, y, z)`
- `ctx.math.add3(x1, y1, z1, x2, y2, z2)`

Examples:

```python
start = ctx.math.vec3(ctx.player.get_pos_x(), ctx.player.get_pos_y() + 1, ctx.player.get_pos_z())
end = ctx.math.add3(ctx.player.get_pos_x(), ctx.player.get_pos_y() + 1, ctx.player.get_pos_z(), 0.0, 0.0, 6.0)
```

```python
distance = ctx.math.distance3(0.0, 64.0, 0.0, ctx.player.get_pos_x(), ctx.player.get_pos_y(), ctx.player.get_pos_z())
```

## Raycast Helpers

Available world helpers:

- `ctx.world.raycast_block(start_vec, end_vec)`
- `ctx.world.raycast_block_id(start_vec, end_vec)`
- `ctx.world.raycast_block_pos_x(start_vec, end_vec)`
- `ctx.world.raycast_block_pos_y(start_vec, end_vec)`
- `ctx.world.raycast_block_pos_z(start_vec, end_vec)`

Example:

```python
start = ctx.math.vec3(ctx.player.get_pos_x(), ctx.player.get_pos_y() + 1.6, ctx.player.get_pos_z())
end = ctx.math.add3(ctx.player.get_pos_x(), ctx.player.get_pos_y() + 1.6, ctx.player.get_pos_z(), 0.0, 0.0, 8.0)
looked_block = ctx.world.raycast_block_id(start, end)
```

## Particle Helpers

Available world helpers:

- `ctx.world.spawn_particle(particle_id, x, y, z, dx, dy, dz, speed, count)`
- `ctx.world.spawn_particle_self(particle_id, dx, dy, dz, speed, count)`

Example:

```python
ctx.world.spawn_particle(
    "minecraft:end_rod",
    ctx.player.get_pos_x(),
    ctx.player.get_pos_y() + 1.0,
    ctx.player.get_pos_z(),
    0.0,
    0.1,
    0.0,
    0.0,
    6,
)
```

## Notes

- these helpers are generated cross-loader helpers, not dependency-specific code
- the particle helper currently targets simple particle ids cleanly
- the raycast helpers are aimed at block-hit queries first
