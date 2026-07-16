# API Reference

This page contains the API Reference for the core public classes and methods in DryGram.

## DryClient

`class drygram.DryClient(session, api_id, api_hash, bot_token=None, proxy=None, use_ipv6=False)`

The main asynchronous client engine.

### Constructor Parameters

- **session** (`Union[str, Session]`): Session identifier filename (for default SQLite backend) or a concrete `Session` subclass instance.
- **api_id** (`int`): Your API ID from my.telegram.org.
- **api_hash** (`str`): Your API Hash from my.telegram.org.
- **bot_token** (`Optional[str]`, default `None`): Optional bot token for bot logins.
- **proxy** (`Optional[dict]`, default `None`): Proxy configuration dict.
- **use_ipv6** (`bool`, default `False`): Connect to Telegram servers using IPv6.

### Public Methods

#### `async start()`
Starts the client connection pool, loads the session database, and initializes the update dispatcher.

#### `async stop()`
Closes active sockets and saves session metadata.

#### `async request_login_code(phone_number)`
Requests Telegram to send a verification code.
- **phone_number** (`str`): Phone number in international format.
- **Returns**: `str` (phone code hash).

#### `async complete_login(phone_number, phone_code_hash, phone_code)`
Completes user authentication.
- **phone_number** (`str`): User phone number.
- **phone_code_hash** (`str`): Verification hash.
- **phone_code** (`str`): Code received.
- **Returns**: `User` object.

#### `async deliver(chat_id, text, parse_mode="markdown", schedule_date=None)`
Delivers a text message to a chat.
- **chat_id** (`Union[int, str]`): Target chat ID or username.
- **text** (`str`): Message text.
- **Returns**: `Message` object.

#### `async deliver_image(chat_id, file, caption=None)`
Delivers an image.
- **chat_id** (`Union[int, str]`): Target chat.
- **file** (`Union[str, bytes]`): File path or binary bytes.
- **Returns**: `Message` object.

#### `async upload(file_path)`
Uploads a file to Telegram servers.
- **Returns**: `str` (uploaded file ID).

---

## Session

`class drygram.sessions.Session()`

The base session class.

### Attributes
- **dc_id** (`int`): Data center ID.
- **server_address** (`str`): Server IP address.
- **server_port** (`int`): Server port.
- **auth_key** (`Optional[bytes]`): Authorization key bytes.
- **user_id** (`Optional[int]`): Authorized User ID.
- **is_bot** (`bool`): True if authorized as a bot.
- **auth_state** (`str`): Session auth state ("unauthorized", "authorized", "destroyed").
