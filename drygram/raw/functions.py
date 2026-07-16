# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from drygram.raw.parser import TLObject, TLRegistry


@TLRegistry.register
class PingDelayDisconnect(TLObject):
    CONSTRUCTOR_ID = 0xf3427b7c
    FIELDS = [("ping_id", "long"), ("disconnect_delay", "int")]

    def __init__(self, ping_id=0, disconnect_delay=60):
        self.ping_id = ping_id
        self.disconnect_delay = disconnect_delay


@TLRegistry.register
class SendCode(TLObject):
    CONSTRUCTOR_ID = 0xa677244f
    FIELDS = [
        ("phone_number", "string"),
        ("api_id", "int"),
        ("api_hash", "string"),
        ("settings", "Object")
    ]

    def __init__(self, phone_number="", api_id=0, api_hash="", settings=None):
        self.phone_number = phone_number
        self.api_id = api_id
        self.api_hash = api_hash
        self.settings = settings


@TLRegistry.register
class SignIn(TLObject):
    CONSTRUCTOR_ID = 0xbcd51581
    FIELDS = [
        ("phone_number", "string"),
        ("phone_code_hash", "string"),
        ("phone_code", "string")
    ]

    def __init__(self, phone_number="", phone_code_hash="", phone_code=""):
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.phone_code = phone_code


@TLRegistry.register
class LogOut(TLObject):
    CONSTRUCTOR_ID = 0x3fc70190
    FIELDS = []


@TLRegistry.register
class GetAuthorizations(TLObject):
    CONSTRUCTOR_ID = 0xe320c158
    FIELDS = []
