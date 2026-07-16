# Callback Queries

DryGram supports receiving and answering callback queries sent by users when they click inline keyboard buttons.

## Observing Callback Queries

You can observe callback queries using the Gates and dispatcher observers:

```python
from drygram import Gates, Message

# Observe callback buttons clicked by users
@app.observe(Gates.callback())
async def button_click_handler(update):
    print(f"User clicked button with data: {update.data}")
    # Answer callback query to stop loading state on Telegram client
    await update.answer("Action received!")
```

## Inline Callback Gates

Filter callback events based on data payloads:

```python
# Match callback queries where data equals 'confirm_action'
confirm_gate = Gates.callback("confirm_action")
```
