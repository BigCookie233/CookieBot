# coding: utf-8

# Created by BigCookie233

import CookieLibraries.BotController as BotController
import CookieLibraries.Events as Events


# Message Segment Classes
class MessageSegment:
    def __init__(self, msg_type):
        self.msg_type = msg_type

    @property
    def data(self) -> dict:
        return {}

    @property
    def raw_segment(self) -> dict:
        return {"type": self.msg_type, "data": self.data}


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
        return {"id": self.msg_id}


# Message Classes
class Message:
    def __init__(self, segment_chain=None):
        if segment_chain is None:
            segment_chain = []
        self.segment_chain = segment_chain

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

    @property
    def raw_message(self):
        chain = []
        for seg in self.segment_chain:
            chain.append(seg.raw_segment)
        return chain

    def send_to_group(self, group_id):
        Events.SendGroupMessageEvent(self.raw_message, group_id).call()


parser_map = {
    "text": lambda data: TextSegment(data["text"]),
    "face": lambda data: FaceSegment(data["id"]),
    "image": lambda data: ImageSegment(data["file"]),
    "at": lambda data: AtSegment(data["qq"]),
    "reply": lambda data: ReplySegment(data["id"])
}


class ReceivedMessage(Message):
    def __init__(self, raw_msg, msg_id, sender):
        chain = []
        for seg in raw_msg:
            msg_type = seg["type"]
            data = seg["data"]
            if msg_type in parser_map.keys():
                chain.append(parser_map[msg_type](data))
        super().__init__(chain)
        self.message_id = msg_id
        self.sender = sender


class ReceivedGroupMessage(ReceivedMessage):
    def __init__(self, raw_msg, msg_id, sender, group_id):
        super().__init__(raw_msg, msg_id, sender)
        self.group_id = group_id
