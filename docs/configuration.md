# Client Configurations

DryGram offers detailed configuration flags to control connection timeouts, transport selection, worker threads, and proxy settings.

## Basic Configurations

Set connection properties on `DryClient`:

```python
client = DryClient(
    "session_name",
    api_id=123,
    api_hash="abc",
    use_ipv6=True,
    proxy={"scheme": "socks5", "hostname": "127.0.0.1", "port": 1080}
)
```
