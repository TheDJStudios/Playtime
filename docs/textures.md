# Textures

Texture PNG files live in your repo under `assets/<modid>/textures/...`.

Folders:

- block textures: `assets/<modid>/textures/block/...`
- item textures: `assets/<modid>/textures/item/...`

Emissive companion textures:

- block emissive overlays live alongside normal block textures
- item emissive overlays live alongside normal item textures
- the usual naming pattern is something like `lamp.png` and `lamp_em.png`

How `texture = ...` resolves:

- on `mc.Block`, `texture = "decor/lamp"` means:
  `assets/<modid>/textures/block/decor/lamp.png`
- on `mc.Item`, `texture = "food/pickle"` means:
  `assets/<modid>/textures/item/food/pickle.png`
- namespaced ids inside manual JSON like `"mymod:block/decor/lamp"` refer to the texture id directly, not to a filesystem path string

Examples:

- item:
  `texture = "food/pickle"`
  file:
  `assets/<modid>/textures/item/food/pickle.png`
- block:
  `texture = "block/block"`
  file:
  `assets/<modid>/textures/block/block.png`
- block emissive overlay:
  `emissive_texture = "block/block_em"`
  file:
  `assets/<modid>/textures/block/block_em.png`

Compile behavior:

- repo textures are copied into each generated loader project
- repo assets are the source of truth
- `.fabricpy_build/` is generated output and should not be your main authoring location

Recommended sizes:

- `16x16`
- `32x32`
- `64x64`

Troubleshooting:

- item has missing texture:
  check the generated or overridden item model under `assets/<modid>/models/item/...`
  make sure `layer0` points at `<modid>:item/...`
- block has missing texture:
  check the block model under `assets/<modid>/models/block/...`
  make sure the model texture entry points at `<modid>:block/...`
- block breaks with missing particles:
  the block model needs a `particle` texture entry
  for simple cube blocks, set `"particle": "<modid>:block/<path>"`
- the Python `texture` field looks right but Minecraft still shows purple/black:
  a repo-level `models/block/*.json` or `models/item/*.json` file may be overriding the generated model and pointing at the wrong texture id
