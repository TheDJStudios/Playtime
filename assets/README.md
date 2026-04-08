# Assets Folder

Put source resource-pack files here, namespaced by `mod_id`.

Example:

```text
assets/
  test/
    textures/
      block/
        test/
          block.png
      item/
        food/
          pickle.png
    models/
      block/
        custom_block.json
      item/
        custom_item.json
    blockstates/
      custom_block.json
    lang/
      en_us.json
```

During compile, `fabricpy` copies `assets/<modid>/...` into both generated projects:

- `src/main/resources/assets/<modid>/...` for Fabric
- `src/main/resources/assets/<modid>/...` for Forge

Copied files override generated defaults when paths collide.
