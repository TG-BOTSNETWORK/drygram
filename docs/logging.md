# Logging Configurations

DryGram implements standard Python logging outputs.

## Setup Logging

Configure log formatters to track network handshakes and dispatcher activities:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```
