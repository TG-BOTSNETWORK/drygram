# Core Architecture

DryGram is built as a pure asynchronous, decoupled framework.

## Component Layers

1. **Transport Layer**: Dispatches raw packets using TCP/HTTP connection drivers.
2. **MTProto RPC Layer**: Encrypts payloads and tracks sequence numbers.
3. **Dispatcher**: Observes signal pipelines using boolean gates.
4. **Storage Engine**: Persists session parameters across pluggable drivers.
