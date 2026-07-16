# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import struct
from typing import Any, List, Dict, Optional, Type, Tuple


class TLObject:
    CONSTRUCTOR_ID: int = 0
    FIELDS: List[Tuple[str, str]] = []

    def serialize(self) -> bytes:
        payload = bytearray()
        payload.extend(struct.pack("<I", self.CONSTRUCTOR_ID))

        flags_val = 0
        has_flags = False
        flags_field_index = -1

        for idx, (name, f_type) in enumerate(self.FIELDS):
            if f_type == "flags":
                has_flags = True
                flags_field_index = idx
                continue

            if "?" in f_type:
                flag_part, actual_type = f_type.split("?")
                bit_idx = int(flag_part.split(".")[1])
                val = getattr(self, name, None)
                if val is not None and val is not False:
                    flags_val |= (1 << bit_idx)

        for idx, (name, f_type) in enumerate(self.FIELDS):
            if idx == flags_field_index:
                payload.extend(struct.pack("<I", flags_val))
                continue

            val = getattr(self, name, None)
            if "?" in f_type:
                flag_part, actual_type = f_type.split("?")
                bit_idx = int(flag_part.split(".")[1])
                if not (flags_val & (1 << bit_idx)):
                    continue
                f_type = actual_type

            payload.extend(self._serialize_value(val, f_type))

        return bytes(payload)

    @classmethod
    def _serialize_value(cls, val: Any, f_type: str) -> bytes:
        if f_type == "int":
            return struct.pack("<i", val)
        elif f_type == "long":
            return struct.pack("<q", val)
        elif f_type == "double":
            return struct.pack("<d", val)
        elif f_type == "string":
            b = val.encode("utf-8") if isinstance(val, str) else val
            return cls._serialize_bytes(b)
        elif f_type == "bytes":
            return cls._serialize_bytes(val)
        elif f_type == "Bool":
            if val:
                return struct.pack("<I", 0x997275b5)
            else:
                return struct.pack("<I", 0xbc799737)
        elif f_type.startswith("Vector<"):
            inner_type = f_type[7:-1]
            out = bytearray()
            out.extend(struct.pack("<I", 0x1cb5c415))
            out.extend(struct.pack("<i", len(val)))
            for item in val:
                out.extend(cls._serialize_value(item, inner_type))
            return bytes(out)
        elif isinstance(val, TLObject):
            return val.serialize()
        else:
            raise ValueError(f"Unknown type to serialize: {f_type}")

    @staticmethod
    def _serialize_bytes(val: bytes) -> bytes:
        length = len(val)
        if length < 254:
            res = bytes([length]) + val
        else:
            res = b'\xfe' + struct.pack("<I", length)[:3] + val
        padding = (4 - len(res) % 4) % 4
        return res + b'\x00' * padding


class TLRegistry:
    CONSTRUCTORS: Dict[int, Type[TLObject]] = {}

    @classmethod
    def register(cls, obj_cls: Type[TLObject]) -> Type[TLObject]:
        cls.CONSTRUCTORS[obj_cls.CONSTRUCTOR_ID] = obj_cls
        return obj_cls


class TLDeserializer:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def deserialize(self) -> Any:
        if self.offset >= len(self.data):
            return None
        
        cid = struct.unpack_from("<I", self.data, self.offset)[0]
        self.offset += 4

        if cid == 0x997275b5:
            return True
        elif cid == 0xbc799737:
            return False
        elif cid == 0x3072cfa1:
            import gzip
            packed_data = self._deserialize_bytes()
            decompressed = gzip.decompress(packed_data)
            return TLDeserializer(decompressed).deserialize()
        elif cid == 0x73f1f8dc:
            count = struct.unpack_from("<i", self.data, self.offset)[0]
            self.offset += 4
            messages = []
            for _ in range(count):
                msg_id, seqno, m_len = struct.unpack_from("<qii", self.data, self.offset)
                self.offset += 16
                body_bytes = self.data[self.offset:self.offset+m_len]
                self.offset += m_len
                body = TLDeserializer(body_bytes).deserialize()
                messages.append({
                    "msg_id": msg_id,
                    "seqno": seqno,
                    "body": body
                })
            return MsgContainer(messages)
        elif cid == 0x1cb5c415:
            count = struct.unpack_from("<i", self.data, self.offset)[0]
            self.offset += 4
            result = []
            for _ in range(count):
                result.append(self.deserialize())
            return result

        cls_type = TLRegistry.CONSTRUCTORS.get(cid)
        if not cls_type:
            return TLOpaqueObject(cid, self._read_remaining())

        obj = cls_type()
        flags_val = 0

        for name, f_type in cls_type.FIELDS:
            if f_type == "flags":
                flags_val = struct.unpack_from("<I", self.data, self.offset)[0]
                self.offset += 4
                setattr(obj, name, flags_val)
                continue

            if "?" in f_type:
                flag_part, actual_type = f_type.split("?")
                bit_idx = int(flag_part.split(".")[1])
                if not (flags_val & (1 << bit_idx)):
                    setattr(obj, name, None)
                    continue
                f_type = actual_type

            val = self._deserialize_value(f_type)
            setattr(obj, name, val)

        return obj

    def _deserialize_value(self, f_type: str) -> Any:
        if f_type == "int":
            val = struct.unpack_from("<i", self.data, self.offset)[0]
            self.offset += 4
            return val
        elif f_type == "long":
            val = struct.unpack_from("<q", self.data, self.offset)[0]
            self.offset += 8
            return val
        elif f_type == "double":
            val = struct.unpack_from("<d", self.data, self.offset)[0]
            self.offset += 8
            return val
        elif f_type == "string":
            return self._deserialize_bytes().decode("utf-8", errors="replace")
        elif f_type == "bytes":
            return self._deserialize_bytes()
        elif f_type == "Bool":
            cid = struct.unpack_from("<I", self.data, self.offset)[0]
            self.offset += 4
            return cid == 0x997275b5
        elif f_type.startswith("Vector<"):
            inner_type = f_type[7:-1]
            cid = struct.unpack_from("<I", self.data, self.offset)[0]
            self.offset += 4
            if cid != 0x1cb5c415:
                raise ValueError("Expected vector constructor ID")
            count = struct.unpack_from("<i", self.data, self.offset)[0]
            self.offset += 4
            result = []
            for _ in range(count):
                result.append(self._deserialize_value(inner_type))
            return result
        else:
            return self.deserialize()

    def _deserialize_bytes(self) -> bytes:
        first = self.data[self.offset]
        if first < 254:
            length = first
            self.offset += 1
        else:
            length = struct.unpack_from("<I", self.data[self.offset:self.offset+4] + b'\x00')[0] >> 8
            self.offset += 4
        val = self.data[self.offset:self.offset+length]
        self.offset += length
        padding = (4 - (length + (1 if first < 254 else 4)) % 4) % 4
        self.offset += padding
        return val

    def _read_remaining(self) -> bytes:
        val = self.data[self.offset:]
        self.offset = len(self.data)
        return val


class TLOpaqueObject(TLObject):
    def __init__(self, constructor_id: int, data: bytes):
        self.CONSTRUCTOR_ID = constructor_id
        self.data = data

    def serialize(self) -> bytes:
        return struct.pack("<I", self.CONSTRUCTOR_ID) + self.data


class MsgContainer(TLObject):
    CONSTRUCTOR_ID = 0x73f1f8dc

    def __init__(self, messages: Optional[List[dict]] = None):
        self.messages = messages or []

    def serialize(self) -> bytes:
        payload = bytearray()
        payload.extend(struct.pack("<I", self.CONSTRUCTOR_ID))
        payload.extend(struct.pack("<i", len(self.messages)))
        for msg in self.messages:
            msg_bytes = msg["body"].serialize()
            payload.extend(struct.pack("<qii", msg["msg_id"], msg["seqno"], len(msg_bytes)))
            payload.extend(msg_bytes)
        return bytes(payload)
