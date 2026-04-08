# Interop

This page describes the advanced compiler side of FabricPy.

The short version:

- the normal Python API is still the main path
- the compiler now also has an early dependency interop system
- that interop system can now resolve dependency classes, static methods, static fields, and constructor calls from the scanned symbol index
- it is still not a full typed Java frontend yet

## Current Architecture

Today, the dependency interop flow looks like this:

1. dependencies are declared or auto-injected by generated features
2. generated projects write `.fabricpy_meta/interop_project.json`
3. successful builds scan resolved dependency jars
4. the scanner writes:
   - `symbol_index.json`
   - `.pyi` stubs under `python_stubs/dep/...`
5. the transpiler uses a resolver layer to understand `dep.<alias>...` references
6. dependency calls are checked against scanned class/member data when possible

## Current Interop Surface

The current low-level escape hatch is:

```python
dep.<alias>.<java package>.<Class>.<member>
```

Examples:

```python
dep.geckolib.software.bernie.geckolib.core.animation.RawAnimation.begin()
```

That becomes:

```java
software.bernie.geckolib.core.animation.RawAnimation.begin();
```

Constructor calls are now handled too:

```python
dep.somealias.com.example.Widget("hello")
```

If `com.example.Widget` is present in the scanned symbol index as a class, that becomes:

```java
new com.example.Widget("hello");
```

## Resolver Layer

FabricPy now includes a dedicated resolver between the symbol index and the transpiler.

Its current job is to:

- understand dependency aliases
- resolve known class names from the scanned index
- match static methods and fields when present in scanned class detail
- recognize class calls as constructors
- attach compiler notes when a dependency call is only partially validated
- fall back to best-effort Java path emission when full typed resolution is not available yet

This is the important shift from pure passthrough to actual compiler-assisted dependency path handling.

## What Gets Validated Today

When a dependency symbol index is present, the resolver can currently validate:

- whether a dependency alias exists
- whether a class exists under that alias
- whether a named member exists on that class
- whether a static method with the requested argument count exists
- whether a constructor with the requested argument count exists

This means FabricPy can now distinguish between cases like:

- `dep.alias.pkg.Class()`:
  treated as a constructor call and emitted as `new pkg.Class()`
- `dep.alias.pkg.Class.make()`:
  treated as a static factory call when the scanner sees a matching static method
- `dep.alias.pkg.Class.instanceMethod()`:
  emitted, but marked with an interop note because it looks like an instance method called on the class

## Interop Notes

When the compiler can resolve part of a dependency call but cannot fully prove it is correct, it now leaves a Java comment near the generated code.

Typical cases:

- the member exists, but only as an instance method
- the class exists, but the requested constructor arity was not found
- the call chain extends past a scanned class/member boundary

These notes are there to make interop debugging faster without failing the whole compile.

## Current Limits

This is still not the final form of the interop system.

Important limits that still remain:

- overloads are matched only by argument count, not full parameter types
- return types are scanned, but not yet used for downstream expression typing
- instance/member chaining after the first resolved boundary is still best-effort
- core Minecraft and loader jars are still intentionally not part of this dependency scanner pass
- Python `import` syntax for dependency namespaces is still a future phase

So the correct current mental model is:

- dependency discovery: real
- dependency call resolution: real
- constructor emission: real
- typed semantic interop: partial
