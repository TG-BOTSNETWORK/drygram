# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
import time
import struct
from typing import Dict, List, Any
from drygram.raw import TLObject, TLDeserializer, MsgContainer, Ping, Pong, MsgsAck, BadMsgNotification, BadServerSalt, RpcResult
from drygram.sessions.session import Session
from drygram.errors.rpc import from_rpc_error, NetworkError


class MTProtoEngine:
    def __init__(self, session: Session):
        self.session = session
        self.time_offset = 0
        self.seq_no = 0
        self.pending_rpcs: Dict[int, asyncio.Future] = {}
        self.ack_queue: List[int] = []
        self._lock = asyncio.Lock()

    def generate_msg_id(self) -> int:
        now = time.time() + self.time_offset
        msg_id = int(now * (2 ** 32))
        # Client messages must be divisible by 4
        msg_id = (msg_id & ~3) | 0
        return msg_id

    def generate_seq_no(self, content_related: bool) -> int:
        seq = self.seq_no * 2
        if content_related:
            seq += 1
            self.seq_no += 1
        return seq

    def sync_time(self, server_time: int) -> None:
        local_time = int(time.time())
        self.time_offset = server_time - local_time

    async def send_rpc(self, request: TLObject, connection=None) -> Any:
        fut = asyncio.get_running_loop().create_future()
        msg_id = self.generate_msg_id()
        seq_no = self.generate_seq_no(True)

        async with self._lock:
            self.pending_rpcs[msg_id] = fut

        # If connection is supplied, write data
        if connection:
            payload = request.serialize()
            # Wrap with MTProto message layer: auth_key_id + message_id + seq_no + message_data_length + payload
            # For unencrypted/initial requests or simple mock queries
            msg_header = struct.pack("<qii", msg_id, seq_no, len(payload))
            await connection.write(msg_header + payload)

        return await fut

    def process_incoming_payload(self, payload: bytes) -> None:
        try:
            obj = TLDeserializer(payload).deserialize()
        except Exception:
            return

        if isinstance(obj, MsgContainer):
            for msg in obj.messages:
                self.ack_queue.append(msg["msg_id"])
                self._handle_message(msg["body"], msg["msg_id"])
        elif obj:
            self._handle_message(obj, 0)

    def _handle_message(self, obj: Any, msg_id: int) -> None:
        if isinstance(obj, Pong):
            pass
        elif isinstance(obj, RpcResult):
            fut = self.pending_rpcs.pop(obj.req_msg_id, None)
            if fut and not fut.done():
                if isinstance(obj.result, bytes) and obj.result.startswith(b'\x01\x14\xec\x08'):
                    # RPC Error constructor ID
                    try:
                        err_obj = TLDeserializer(obj.result).deserialize()
                        fut.set_exception(from_rpc_error(err_obj.error_code, err_obj.error_message))
                    except Exception as e:
                        fut.set_exception(e)
                else:
                    fut.set_value(obj.result)
        elif isinstance(obj, BadServerSalt):
            self.session.server_salt = obj.new_server_salt
            # Resend sequence would trigger here in a full connection loop
        elif isinstance(obj, BadMsgNotification):
            # Handle bad message notification code (e.g. time out of sync)
            pass
