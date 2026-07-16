# DryGram Command Framework API Documentation

The DryGram Command Framework is a production-grade, highly extensible, and fully asynchronous architecture designed to handle chat command routing, parameter parsing, type conversion, custom validations, rate limiting, and permissions checks.

---

## 1. Core API Reference

### `command` (Decorator)
Decorates and registers a function as a Command.

* **Description**: Declares a command trigger name, aliases, description, and execution rules.
* **Parameters**:
  * `name` (str): Primary name trigger of the command.
  * `aliases` (Optional[List[str]]): Additional trigger names.
  * `description` (str): Help description text.
  * `category` (str): Category group (default: "General").
  * `owner_only` (bool): Restrict execution to the bot owner.
  * `admin_only` (bool): Restrict execution to chat administrators.
  * `premium_only` (bool): Restrict to Telegram Premium users.
  * `business_only` (bool): Restrict to Telegram Business connections.
  * `private_only` (bool): Restrict to private chat contexts.
  * `group_only` (bool): Restrict to group/supergroup contexts.
  * `channel_only` (bool): Restrict to channel contexts.
  * `topic_only` (bool): Restrict to forum thread topics.
  * `cooldown_rate` (int): Number of permitted calls within the cooldown window (default: 1).
  * `cooldown_per` (float): Duration in seconds of the cooldown window.
* **Returns**: Decorated callable wrapper.
* **Example**:
  ```python
  from drygram.commands import command, CommandContext

  @command("ban", admin_only=True, cooldown_per=5.0)
  async def ban_user(ctx: CommandContext, user_id: int):
      await ctx.respond(f"Banned user {user_id}")
  ```

---

### `CommandRouter`
The orchestrator that registers to the client's event loop and routes incoming message events.

* **Description**: Matches prefixes, parses tokens, verifies permissions and cooldowns, maps typed arguments, and runs commands.
* **Parameters**:
  * `client` (DryClient): The active DryClient instance.
  * `registry` (Optional[CommandRegistry]): Custom registry to bind (uses global registry if omitted).
* **Methods**:
  * `route(client, message) -> bool`: Directly routes and runs a message command.
* **Example**:
  ```python
  from drygram import DryClient
  from drygram.commands import CommandRouter

  client = DryClient("session")
  router = CommandRouter(client)
  ```

---

### `RichText` & builders
High-level chainable markup builder.

* **Description**: Easily build formatted text representations.
* **Methods**:
  * `text(val)` / `bold(val)` / `italic(val)` / `underline(val)` / `strikethrough(val)` / `spoiler(val)` / `code(val)` / `code_block(val, language)` / `blockquote(val, expandable)` / `link(label, url)` / `mention(label, user_id)` / `emoji(char, emoji_id)`
  * `to_markdown()` -> str (MarkdownV2 compilation)
  * `to_html()` -> str (HTML compilation)
* **Example**:
  ```python
  from drygram.commands import RichText

  rt = RichText().bold("Status:").text(" ").italic("Active")
  print(rt.to_html()) # <b>Status:</b> <i>Active</i>
  ```

---

## 2. Best Practices
1. **Always Type Annotate**: Always add type annotations to your command callback parameters so that the `CommandExecutor` can auto-convert arguments correctly (e.g. `user_id: int` instead of just `user_id`).
2. **Handle Exceptions Gracefully**: Unhandled exceptions inside commands are captured, logged, and output to the user. To override default error output, catch exceptions inside your handlers.
3. **Use HTML for Layouts**: HTML tags are generally easier to nest and read than escaping complex MarkdownV2 strings.

---

## 3. Migration Guide

If migrating from older client frameworks, replace standard event filters with CommandRouter routing:

**Before (Legacy)**:
```python
@client.on(events.NewMessage(pattern="/ban"))
async def legacy_ban(event):
    ...
```

**After (DryGram Command Framework)**:
```python
from drygram.commands import command, CommandContext

@command("ban", admin_only=True)
async def new_ban(ctx: CommandContext, user_id: int):
    ...
```
