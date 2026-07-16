# Keyboards & Markups

DryGram supports adding custom Reply Keyboards (buttons replacing client input) and Inline Keyboards (buttons attached directly to messages).

## Inline Keyboards

Inline keyboards are attached to sent messages and trigger callback query events:

```python
from drygram.types.markup import InlineKeyboardMarkup, InlineKeyboardButton

# Create Inline Keyboard layout
markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Help Menu", callback_data="help_data"),
        InlineKeyboardButton("Visit Website", url="https://telegram.org")
    ]
])

# Deliver message with inline keyboard markup
await client.deliver(123456, "Choose an option:", markup=markup)
```

## Reply Keyboards

Reply keyboards replace the standard user input box with customizable buttons:

```python
from drygram.types.markup import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup([
    [KeyboardButton("Send Contact", request_contact=True)],
    [KeyboardButton("Send Location", request_location=True)]
], resize_keyboard=True, one_time_keyboard=True)

await client.deliver(123456, "Provide information:", markup=markup)
```
