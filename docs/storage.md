# Storage Backend Architecture

DryGram separates session states and metadata persistence into decoupled, modular storage backends.

## Pluggable Drivers

Storage backends inherit from the core `Session` class and implement standard read/write interfaces to persist credentials:

- **Local Storage**: Built-in JSON, Binary, Encrypted Binary, or SQLite engines.
- **Remote Databases**: Scale horizontally using Postgres, Redis, or MongoDB backends.
- **Custom Backends**: Define custom callback hooks (`CustomSession`) to query external APIs or vaults.
