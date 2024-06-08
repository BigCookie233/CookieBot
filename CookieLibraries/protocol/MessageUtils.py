# coding: utf-8
# Created by BigCookie233
from ..core import EventManager
from . import BotController


# Message Segment Classes
class MessageSegment:
    def __init__(self, msg_type):
        self.msg_type = msg_type

    def extend(self, other):
        if isinstance(other, MessageSegment):
            return MessageBuilder([self, other])
        elif isinstance(other, MessageBuilder):
            return MessageBuilder([self].extend(other.segment_chain))

    def __add__(self, other):
        return self.extend(other)

    @property
    def raw_segment(self) -> dict:
        return {"type": self.msg_type, "data": self.data}

    @property
    def data(self) -> dict:
        raise NotImplementedError


class TextSegment(MessageSegment):
    def __init__(self, text):
        self.text = text
        super().__init__("text")

    @property
    def data(self):
        return {"text": self.text}

    def __eq__(self, other):
        if isinstance(other, TextSegment):
            return self.text == other.text
        elif isinstance(other, str):
            return self.text == other


class FaceSegment(MessageSegment):
    def __init__(self, face_id):
        self.face_id = face_id
        super().__init__("face")

    @property
    def data(self):
        return {"id": self.face_id}


class ImageSegment(MessageSegment):
    def __init__(self, file):
        self.file = file
        super().__init__("image")

    @property
    def data(self):
        return {"file": self.file}


class AtSegment(MessageSegment):
    def __init__(self, qq):
        self.qq = qq
        super().__init__("at")

    @property
    def data(self):
        return {"qq": str(self.qq)}


class ReplySegment(MessageSegment):
    def __init__(self, msg_id):
        self.msg_id = msg_id
        super().__init__("reply")

    @property
    def data(self):
        return {"id": str(self.msg_id)}


# Message Classes
class Message:
    def __init__(self, seg_chain: list):
        self.segment_chain = seg_chain

    def startswith_atme(self):
        return self.segment_chain and isinstance(self.segment_chain[0], AtSegment) and self.segment_chain[0].qq == str(
            BotController.get_login_info()["user_id"])

    def send_to_group(self, group_id):
        BotController.SendGroupMessageEvent(self.raw_message, group_id).call()

    @property
    def raw_message(self):
        chain = []
        for seg in self.segment_chain:
            chain.append(seg.raw_segment)
        return chain


class MessageBuilder(Message):
    def __init__(self, seg_chain: list = None):
        if seg_chain is None:
            seg_chain = []
        super().__init__(seg_chain)

    def text(self, text):
        self.segment_chain.append(TextSegment(text))
        return self

    def face(self, face_id):
        self.segment_chain.append(FaceSegment(face_id))
        return self

    def image(self, file):
        self.segment_chain.append(ImageSegment(file))
        return self

    def at(self, qq):
        self.segment_chain.append(AtSegment(qq))
        return self

    def reply(self, msg_id):
        self.segment_chain.append(ReplySegment(msg_id))
        return self

    def extend(self, other):
        if isinstance(other, MessageSegment):
            self.segment_chain.append(other)
            return self
        elif isinstance(other, MessageBuilder):
            self.segment_chain.extend(other.segment_chain)
            return self

    def __add__(self, other):
        return self.extend(other)


class ReceiveMessageEvent(Message, EventManager.Event):
    def __init__(self, raw_msg, msg_id, sender):
        chain = []
        for seg in raw_msg:
            msg_type = seg["type"]
            data = seg["data"]
            match msg_type:
                case "text":
                    chain.append(TextSegment(data["text"]))
                case "face":
                    chain.append(FaceSegment(data["id"]))
                case "image":
                    chain.append(ImageSegment(data["file"]))
                case "at":
                    chain.append(AtSegment(data["qq"]))
                case "reply":
                    chain.append(ReplySegment(data["id"]))
        super().__init__(chain)
        self.message_id = msg_id
        self.sender = sender


class ReceiveGroupMessageEvent(ReceiveMessageEvent):
    def __init__(self, raw_msg, msg_id, sender):
        super().__init__(raw_msg, msg_id, sender)
