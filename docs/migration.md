# Migration Guide

This guide assists developers in migrating codebase projects from other Telegram frameworks (such as Pyrogram or Telethon) to DryGram.

## Differences in API Call Names

DryGram features an original naming architecture:

- **Send Message**: Use `deliver(chat_id, text)` instead of `send_message`.
- **Observers/Event decorators**: Use `@app.observe(Gates.private())` instead of `@app.on_message()`.
- **Middlewares**: Use `@app.middleware()` instead of custom pipeline wrappers.
