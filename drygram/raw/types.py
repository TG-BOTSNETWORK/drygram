# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from drygram.raw.parser import TLObject, TLRegistry


@TLRegistry.register
class MsgsAck(TLObject):
    CONSTRUCTOR_ID = 0x62d6b45e
    FIELDS = [("msg_ids", "Vector<long>")]

    def __init__(self, msg_ids=None):
        self.msg_ids = msg_ids or []


@TLRegistry.register
class Ping(TLObject):
    CONSTRUCTOR_ID = 0x7abe77ec
    FIELDS = [("ping_id", "long")]

    def __init__(self, ping_id=0):
        self.ping_id = ping_id


@TLRegistry.register
class Pong(TLObject):
    CONSTRUCTOR_ID = 0x347773c5
    FIELDS = [("msg_id", "long"), ("ping_id", "long")]

    def __init__(self, msg_id=0, ping_id=0):
        self.msg_id = msg_id
        self.ping_id = ping_id


@TLRegistry.register
class BadMsgNotification(TLObject):
    CONSTRUCTOR_ID = 0xa7efff4c
    FIELDS = [("bad_msg_id", "long"), ("bad_msg_seqno", "int"), ("error_code", "int")]

    def __init__(self, bad_msg_id=0, bad_msg_seqno=0, error_code=0):
        self.bad_msg_id = bad_msg_id
        self.bad_msg_seqno = bad_msg_seqno
        self.error_code = error_code


@TLRegistry.register
class BadServerSalt(TLObject):
    CONSTRUCTOR_ID = 0xed97c512
    FIELDS = [
        ("bad_msg_id", "long"),
        ("bad_msg_seqno", "int"),
        ("error_code", "int"),
        ("new_server_salt", "long")
    ]

    def __init__(self, bad_msg_id=0, bad_msg_seqno=0, error_code=0, new_server_salt=0):
        self.bad_msg_id = bad_msg_id
        self.bad_msg_seqno = bad_msg_seqno
        self.error_code = error_code
        self.new_server_salt = new_server_salt


@TLRegistry.register
class RpcResult(TLObject):
    CONSTRUCTOR_ID = 0xf35c6d01
    FIELDS = [("req_msg_id", "long"), ("result", "Object")]

    def __init__(self, req_msg_id=0, result=None):
        self.req_msg_id = req_msg_id
        self.result = result


@TLRegistry.register
class ResMP(TLObject):
    CONSTRUCTOR_ID = 0x5162463e
    FIELDS = [
        ("nonce", "int128"),
        ("server_nonce", "int128"),
        ("pq", "bytes"),
        ("server_public_key_fingerprints", "Vector<long>")
    ]
