# Callback Buttons

Handle inline keyboard callback queries.

```python
@app.observe(Gates.text("my_callback_data"))
async def callback_handler(msg):
    await app.echo(msg, "Handled!")
```
