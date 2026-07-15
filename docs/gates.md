# Gates (Filters)

Gates define the rules for routing updates.

```python
# Match private chat text starting with /start
Gates.private() & Gates.regex("^/start")
```
