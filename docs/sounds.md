# Sounds

Sound events can be declared from Python and the actual `.ogg` files live in repo assets.

Python method:

- `mod.add_sound(sound_id, sounds, subtitle="", replace=False)`

Arguments:

- `sound_id`: sound event path, for example `"machine/hum"`
- `sounds`: a string path, a list of string paths, a sound entry dict, or a full `sounds.json` entry dict
- `subtitle`: optional subtitle text; `fabricpy` adds the matching lang entry automatically
- `replace`: optional `sounds.json` replace flag

Simple example:

```python
mod.add_sound(
    "machine/hum",
    "machine/hum",
    subtitle="Machine humming",
)
```

That generates a `sounds.json` entry similar to:

```json
{
  "machine/hum": {
    "sounds": [
      {"name": "mymod:machine/hum"}
    ],
    "subtitle": "subtitles.mymod.machine.hum"
  }
}
```

Source file layout:

- sound definitions: `assets/<modid>/sounds.json`
- sound files: `assets/<modid>/sounds/...`

For the example above, the `.ogg` file should be:

- `assets/<modid>/sounds/machine/hum.ogg`

Advanced example:

```python
mod.add_sound(
    "machine/hum",
    [
        {"name": "machine/hum1", "volume": 0.8},
        {"name": "machine/hum2", "volume": 0.8}
    ],
    subtitle="Machine humming",
)
```

Override behavior:

- Python-defined sounds are generated first
- repo `assets/<modid>/sounds.json` is copied after generation
- repo files override generated `sounds.json` if you want full manual control

Playing sounds:

- use `ctx.world.play_sound("mymod:machine/hum", volume, pitch)` from hooks or events

Hook example:

```python
@mod.event("player_use_block")
def on_use(ctx):
    ctx.world.play_sound("mymod:machine/hum", 1.0, 1.0)
```
