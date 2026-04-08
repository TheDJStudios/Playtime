# Compiler Roadmap

The long-term target is a layered Python-to-Minecraft compiler:

- easy for simple mods
- powerful enough for advanced runtime systems
- able to call dependency mod APIs directly without a new wrapper every time

## Layer 1: simple API

- blocks
- items
- entities
- recipes
- sounds
- advancements
- creative tabs
- keybinds
- common events

This is the beginner path and should stay short.

## Layer 2: advanced runtime API

- synced data
- packets/networking
- math and vectors
- raycasts
- particles
- GUI/screens
- render hooks
- code-driven animation
- custom renderers

This is the layer needed for things like GrabPack-style code-driven hands, cables, collision-aware extension, and other advanced gameplay systems.

## Layer 3: direct interop

- declared dependencies
- jar introspection
- generated Python stubs
- typed symbol resolution
- direct calls into Minecraft classes, loader classes, and dependency mod APIs

This is the layer that removes the need to keep adding one-off special support.

## Recommended phases

### Phase 1: dependency foundation

- add `mod.dependency(...)`
- inject repositories and dependency coordinates into generated builds
- emit optional loader metadata

Status:

- started in this repo

### Phase 2: compiler core rewrite

- move beyond hand-written string substitutions
- build a typed IR for Python -> Java
- resolve:
  - fields
  - methods
  - overloads
  - static refs
  - constructors
  - enums
  - imports

### Phase 3: jar introspection

- inspect Minecraft, Fabric, Forge, and dependency jars
- index classes, methods, fields, annotations, and nested classes
- expose that symbol graph to the compiler

Current groundwork:

- generated projects now emit `.fabricpy_meta/interop_project.json`
- generated projects now emit `.fabricpy_meta/symbol_index.stub.json`
- successful builds now also emit:
  - `.fabricpy_meta/symbol_index.json`
  - `.fabricpy_meta/python_stubs/dep/<alias>/...`
- the current scanner resolves dependency jars and indexes top-level package/class names plus public method/field surfaces
- these files are scaffolding for the upcoming typed resolver

### Phase 4: generated stubs

- generate Python-facing modules from the indexed jars
- provide autocomplete and discoverable docs
- expose dependency APIs through Python imports

Current state:

- partial `.pyi` package generation now exists for scanned dependency jars
- those stubs now include scanned method/field surfaces plus basic primitive/string-shaped hints
- the interop resolver now does more than passthrough:
  - class resolution
  - static member resolution
  - constructor emission
  - interop notes for partially validated calls
- full type-safe compilation still is not done yet

Future direction example:

```python
from dep.create.com.simibubi.create import AllBlocks
```

What is still left for the real final phase:

- exact overload resolution by parameter types
- return-type-aware expression typing
- constructor overload selection by type, not just arity
- imported dependency namespaces driving compilation directly
- Minecraft/loader jar indexing alongside dependency jar indexing

### Phase 5: runtime systems

- synced entity data
- synced block data
- packets
- screens
- inventory helpers
- capability/component-style features

### Phase 6: rendering and animation

- entity renderers
- block entity renderers
- code-driven animation
- beam/cable rendering
- model-part access
- client render events

## Design rule

Keep the surface easy:

- declarative defaults first
- advanced escape hatches second
- raw interop only when needed

That keeps beginner code readable while removing the ceiling for advanced mods.
