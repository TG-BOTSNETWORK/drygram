# Performance Optimizations

DryGram is optimized for low latency and high throughput.

## Optimization Strategies

- **Connection Pooling**: Reuses sockets across parallel RPC requests.
- **Dynamic TL Schema**: Serializes binary blocks on the fly without heavy static classes.
- **Concurrent Task Handlers**: Dispatches handler execution to priority pools.
