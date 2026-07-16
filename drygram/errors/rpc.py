# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import re
from typing import Any, Optional, Type, Dict


class DryError(Exception):
    """Base exception class for all DryGram errors."""
    pass


class NetworkError(DryError):
    """
    Exception raised when a network-level error occurs.

    Examples
    --------
    >>> raise NetworkError("Failed to connect to server")
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class TimeoutError(DryError):
    """
    Exception raised when a network operation times out.

    Examples
    --------
    >>> raise TimeoutError("Read operation timed out")
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class RPCError(DryError):
    """
    Base exception class for all Telegram RPC errors.

    Parameters
    ----------
    code : int
        The RPC error code returned by Telegram (e.g. 400, 401, 403, 420).
    message : str
        The raw RPC error message returned by Telegram (e.g. "FLOOD_WAIT_3").
    retry_time : int, default=0
        The number of seconds to wait before retrying, if applicable.
    migration_dc : Optional[int], default=None
        The target Data Center ID to migrate to, if applicable.
    original_rpc_request : Optional[Any], default=None
        The original RPC request object that triggered the error.

    Attributes
    ----------
    error_code : int
        HTTP-like error code.
    error_message : str
        Telegram's error code identifier.
    retry_time : int
        Wait time in seconds.
    migration_dc : Optional[int]
        Target DC ID.
    original_rpc_request : Optional[Any]
        Original request payload.
    """

    def __init__(
        self,
        code: int,
        message: str,
        retry_time: int = 0,
        migration_dc: Optional[int] = None,
        original_rpc_request: Optional[Any] = None
    ):
        self.error_code = code
        self.error_message = message
        self.retry_time = retry_time
        self.migration_dc = migration_dc
        self.original_rpc_request = original_rpc_request
        # Backward compatibility properties
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message} (retry: {retry_time}s, dc: {migration_dc})")


# ==============================================================================
# HTTP-level Exception Classes
# ==============================================================================

class BadRequest(RPCError):
    """
    Exception raised when the request contains invalid parameters (HTTP 400).
    """
    pass


class Unauthorized(RPCError):
    """
    Exception raised when the client is not authorized (HTTP 401).
    """
    pass


class Forbidden(RPCError):
    """
    Exception raised when access to a resource is forbidden (HTTP 403).
    """
    pass


class NotFound(RPCError):
    """
    Exception raised when a resource is not found (HTTP 404).
    """
    pass


class NotAcceptable(RPCError):
    """
    Exception raised when the request is not acceptable (HTTP 406).
    """
    pass


class Flood(RPCError):
    """
    Exception raised when client requests are being rate-limited (HTTP 420).
    """
    pass


class InternalServerError(RPCError):
    """
    Exception raised when an internal server error occurs on Telegram's side (HTTP 500).
    """
    pass


# ==============================================================================
# Concrete RPC Exception Subclasses
# ==============================================================================

class FloodWait(Flood):
    """
    Exception raised when the client must wait before retrying (e.g. FLOOD_WAIT_X).

    Parameters
    ----------
    seconds : int
        The number of seconds to wait before retrying.
    """
    def __init__(self, seconds: int, original_rpc_request: Optional[Any] = None):
        super().__init__(
            code=420,
            message=f"FLOOD_WAIT_{seconds}",
            retry_time=seconds,
            original_rpc_request=original_rpc_request
        )
        self.seconds = seconds


class SlowModeWait(Flood):
    """
    Exception raised when slowmode is enabled in a chat and the client must wait.

    Parameters
    ----------
    seconds : int
        The number of seconds to wait before sending another message.
    """
    def __init__(self, seconds: int, original_rpc_request: Optional[Any] = None):
        super().__init__(
            code=420,
            message=f"SLOWMODE_WAIT_{seconds}",
            retry_time=seconds,
            original_rpc_request=original_rpc_request
        )
        self.seconds = seconds


class RetryAfter(RPCError):
    """
    Exception raised when a temporary block requires retrying after some time.
    """
    def __init__(self, seconds: int, original_rpc_request: Optional[Any] = None):
        super().__init__(
            code=400,
            message=f"RETRY_AFTER_{seconds}",
            retry_time=seconds,
            original_rpc_request=original_rpc_request
        )
        self.seconds = seconds


class UnknownRPCError(RPCError):
    """
    Exception raised when Telegram returns an unknown or unmapped RPC error.
    """
    pass


# ==============================================================================
# Migration RPC Exceptions (HTTP 303 SEE_OTHER)
# ==============================================================================

class PhoneMigrate(RPCError):
    """
    Exception raised when the phone number belongs to another DC.
    """
    def __init__(self, dc_id: int, original_rpc_request: Optional[Any] = None):
        super().__init__(
            code=303,
            message=f"PHONE_MIGRATE_{dc_id}",
            migration_dc=dc_id,
            original_rpc_request=original_rpc_request
        )


class UserMigrate(RPCError):
    """
    Exception raised when the user account belongs to another DC.
    """
    def __init__(self, dc_id: int, original_rpc_request: Optional[Any] = None):
        super().__init__(
            code=303,
            message=f"USER_MIGRATE_{dc_id}",
            migration_dc=dc_id,
            original_rpc_request=original_rpc_request
        )


class FileMigrate(RPCError):
    """
    Exception raised when the requested file is located in another DC.
    """
    def __init__(self, dc_id: int, original_rpc_request: Optional[Any] = None):
        super().__init__(
            code=303,
            message=f"FILE_MIGRATE_{dc_id}",
            migration_dc=dc_id,
            original_rpc_request=original_rpc_request
        )


class StatsMigrate(RPCError):
    """
    Exception raised when the stats statistics are located in another DC.
    """
    def __init__(self, dc_id: int, original_rpc_request: Optional[Any] = None):
        super().__init__(
            code=303,
            message=f"STATS_MIGRATE_{dc_id}",
            migration_dc=dc_id,
            original_rpc_request=original_rpc_request
        )


class SessionError(DryError):
    """Exception raised when a session operation fails or the session is invalid."""
    pass


class AuthError(DryError):
    """Exception raised when authentication fails."""
    pass


# ==============================================================================
# Specific Common Telegram RPC Errors
# ==============================================================================

class AuthKeyUnregistered(Unauthorized):
    """The key is active but has not been registered in the database."""
    pass


class AuthKeyInvalid(Unauthorized):
    """The active auth key is invalid."""
    pass


class SessionExpired(Unauthorized):
    """The current session has expired."""
    pass


class SessionRevoked(Unauthorized):
    """The session was revoked by the user or the server."""
    pass


class UserDeactivated(Unauthorized):
    """The user account has been deleted or deactivated."""
    pass


class PasswordHashInvalid(BadRequest):
    """The 2FA password hash is invalid."""
    pass


class PasswordEmpty(BadRequest):
    """The 2FA password cannot be empty."""
    pass


class PhoneCodeInvalid(BadRequest):
    """The phone confirmation code is invalid."""
    pass


class PhoneCodeExpired(BadRequest):
    """The phone confirmation code has expired."""
    pass


class PhoneNumberInvalid(BadRequest):
    """The phone number is invalid or formatted incorrectly."""
    pass


class PhoneNumberBanned(BadRequest):
    """The phone number has been banned from Telegram."""
    pass


class UsernameInvalid(BadRequest):
    """The requested username is invalid."""
    pass


class UsernameNotOccupied(NotFound):
    """The requested username is not occupied by any user or channel."""
    pass


class ChatIdInvalid(BadRequest):
    """The provided chat identifier is invalid."""
    pass


class PeerIdInvalid(BadRequest):
    """The provided peer identifier is invalid."""
    pass


class ChannelPrivate(Forbidden):
    """The channel is private and cannot be accessed."""
    pass


class ChannelInvalid(BadRequest):
    """The channel object is invalid or inaccessible."""
    pass


class MessageIdInvalid(BadRequest):
    """The provided message identifier is invalid."""
    pass


class MessageNotModified(BadRequest):
    """The message contents were not modified."""
    pass


class MessageEmpty(BadRequest):
    """The message text or attachment cannot be empty."""
    pass


class UserPrivacyRestricted(Forbidden):
    """The target user's privacy settings restrict this action."""
    pass


class ChatWriteForbidden(Forbidden):
    """Writing in this chat is forbidden for the current user."""
    pass


class UserNotMutualContact(Forbidden):
    """The user is not a mutual contact, restricting the action."""
    pass


class BotMethodInvalid(BadRequest):
    """The method is invalid for bot accounts."""
    pass


class BotResponseTimeout(InternalServerError):
    """The bot response timed out on the server."""
    pass


class BotTokenInvalid(BadRequest):
    """The bot token is invalid."""
    pass


class CdnUploadError(InternalServerError):
    """Failed to upload to the CDN server."""
    pass


class CdnDecryptionError(InternalServerError):
    """Failed to decrypt CDN file chunks."""
    pass


class RpcCallFail(InternalServerError):
    """Internal Telegram server error while processing the RPC call."""
    pass


class InternalError(InternalServerError):
    """General internal server error on Telegram side."""
    pass
RPC_ERROR_MAP: Dict[str, Type[RPCError]] = {
    "AUTH_KEY_UNREGISTERED": AuthKeyUnregistered,
    "AUTH_KEY_INVALID": AuthKeyInvalid,
    "SESSION_EXPIRED": SessionExpired,
    "SESSION_REVOKED": SessionRevoked,
    "USER_DEACTIVATED": UserDeactivated,
    "PASSWORD_HASH_INVALID": PasswordHashInvalid,
    "PASSWORD_EMPTY": PasswordEmpty,
    "PHONE_CODE_INVALID": PhoneCodeInvalid,
    "PHONE_CODE_EXPIRED": PhoneCodeExpired,
    "PHONE_NUMBER_INVALID": PhoneNumberInvalid,
    "PHONE_NUMBER_BANNED": PhoneNumberBanned,
    "USERNAME_INVALID": UsernameInvalid,
    "USERNAME_NOT_OCCUPIED": UsernameNotOccupied,
    "CHAT_ID_INVALID": ChatIdInvalid,
    "PEER_ID_INVALID": PeerIdInvalid,
    "CHANNEL_PRIVATE": ChannelPrivate,
    "CHANNEL_INVALID": ChannelInvalid,
    "MSG_ID_INVALID": MessageIdInvalid,
    "MESSAGE_ID_INVALID": MessageIdInvalid,
    "MESSAGE_NOT_MODIFIED": MessageNotModified,
    "MESSAGE_EMPTY": MessageEmpty,
    "USER_PRIVACY_RESTRICTED": UserPrivacyRestricted,
    "CHAT_WRITE_FORBIDDEN": ChatWriteForbidden,
    "USER_NOT_MUTUAL_CONTACT": UserNotMutualContact,
    "BOT_METHOD_INVALID": BotMethodInvalid,
    "BOT_RESPONSE_TIMEOUT": BotResponseTimeout,
    "BOT_TOKEN_INVALID": BotTokenInvalid,
    "CDN_UPLOAD_ERROR": CdnUploadError,
    "CDN_DECRYPTION_ERROR": CdnDecryptionError,
    "RPC_CALL_FAIL": RpcCallFail,
    "INTERNAL_ERROR": InternalError,
}


def from_rpc_error(
    code: int,
    message: str,
    request: Optional[Any] = None
) -> RPCError:
    """
    Parse a raw RPC error code and message into a specific RPCError subclass.

    Parameters
    ----------
    code : int
        The HTTP-like error code returned by Telegram.
    message : str
        The raw error message string returned by Telegram.
    request : Optional[Any], default=None
        The original request object.

    Returns
    -------
    RPCError
        An instance of a specific RPCError subclass.

    Examples
    --------
    >>> err = from_rpc_error(420, "FLOOD_WAIT_30")
    >>> isinstance(err, FloodWait)
    True
    >>> err.seconds
    30
    """
    # 1. Check migrations (303 SEE_OTHER)
    if code == 303:
        for prefix, cls_type in [
            ("PHONE_MIGRATE_", PhoneMigrate),
            ("USER_MIGRATE_", UserMigrate),
            ("FILE_MIGRATE_", FileMigrate),
            ("STATS_MIGRATE_", StatsMigrate)
        ]:
            if message.startswith(prefix):
                try:
                    dc = int(message[len(prefix):])
                    return cls_type(dc_id=dc, original_rpc_request=request)
                except ValueError:
                    pass

    # 2. Check rate limit / wait errors (420 FLOOD)
    if message.startswith("FLOOD_WAIT_"):
        try:
            sec = int(message[11:])
            return FloodWait(seconds=sec, original_rpc_request=request)
        except ValueError:
            pass

    if message.startswith("SLOWMODE_WAIT_"):
        try:
            sec = int(message[14:])
            return SlowModeWait(seconds=sec, original_rpc_request=request)
        except ValueError:
            pass

    if message.startswith("RETRY_AFTER_"):
        try:
            sec = int(message[12:])
            return RetryAfter(seconds=sec, original_rpc_request=request)
        except ValueError:
            pass

    # 3. Check exact match in error map
    if message in RPC_ERROR_MAP:
        return RPC_ERROR_MAP[message](
            code=code,
            message=message,
            original_rpc_request=request
        )

    # 4. Fallback HTTP-level classification
    if code == 400:
        return BadRequest(code, message, original_rpc_request=request)
    elif code == 401:
        return Unauthorized(code, message, original_rpc_request=request)
    elif code == 403:
        return Forbidden(code, message, original_rpc_request=request)
    elif code == 404:
        return NotFound(code, message, original_rpc_request=request)
    elif code == 406:
        return NotAcceptable(code, message, original_rpc_request=request)
    elif code == 420:
        return Flood(code, message, original_rpc_request=request)
    elif code == 500:
        return InternalServerError(code, message, original_rpc_request=request)

    return UnknownRPCError(code, message, original_rpc_request=request)
