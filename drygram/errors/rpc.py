# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

class DryError(Exception):
    pass

class RPCError(DryError):
    def __init__(self, code: int, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message

class FloodWait(RPCError):
    def __init__(self, seconds: int):
        super().__init__(420, f"FLOOD_WAIT_{seconds}")
        self.seconds = seconds

class SessionError(DryError):
    pass

class NetworkError(DryError):
    pass

class AuthError(DryError):
    pass
