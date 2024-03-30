# coding: utf-8

# Created by BigCookie233

import CookieLibraries.BotController as BotController


# Message Segment Classes
class MessageSegment:
    def __init__(self, msg_type):
        self.msg_type = msg_type

    def build_data(self):
        pass

    def build_dict(self):
        return {"type": self.msg_type, "data": self.build_data()}


class TextSegment(MessageSegment):
    def __init__(self, text):
        self.text = text
        super().__init__("text")

    def build_data(self):
        return {"text": self.text}

    def __eq__(self, other):
        if isinstance(other, TextSegment):
            return self.text == other.text
        elif isinstance(other, str):
            return self.text == other


class FaceSegment(MessageSegment):
    def __init__(self, id):
        self.id = id
        super().__init__("face")

    def build_data(self):
        return {"id": self.id}


class ImageSegment(MessageSegment):
    def __init__(self, file):
        self.file = file
        super().__init__("image")

    def build_data(self):
        return {"file": self.file}


class AtSegment(MessageSegment):
    def __init__(self, qq):
        self.qq = qq
        super().__init__("at")

    def build_data(self):
        return {"qq": str(self.qq)}


class ReplySegment(MessageSegment):
    def __init__(self, id):
        self.id = id
        super().__init__("reply")

    def build_data(self):
        return {"id": self.id}


# Message Classes
class Message:
    def __init__(self, segment_chain=None):
        if segment_chain is None:
            segment_chain = []
        self.segment_chain = segment_chain

    def text(self, text):
        self.segment_chain.append(TextSegment(text))
        return self

    def face(self, id):
        self.segment_chain.append(FaceSegment(id))
        return self

    def image(self, file):
        self.segment_chain.append(ImageSegment(file))
        return self

    def at(self, qq):
        self.segment_chain.append(AtSegment(qq))
        return self

    def reply(self, id):
        self.segment_chain.append(ReplySegment(id))

    def build_chain(self):
        chain = []
        for segment in self.segment_chain:
            chain.append(segment.build_dict())
        return chain

    def send_to_group(self, group_id):
        BotController.send_group_message(group_id, self.build_chain())


class ReceivedMessage(Message):
    def __init__(self, raw_msg, msg_id, sender):
        segment_chain = []
        for segment in raw_msg:
            msg_type = segment["type"]
            data = segment["data"]
            if msg_type == "text":
                segment_chain.append(TextSegment(data["text"]))
            elif msg_type == "face":
                segment_chain.append(FaceSegment(data["id"]))
            elif msg_type == "image":
                segment_chain.append(ImageSegment(data["file"]))
            elif msg_type == "at":
                segment_chain.append(TextSegment(data["qq"]))
            elif msg_type == "reply":
                segment_chain.append(TextSegment(data["id"]))
        super().__init__(segment_chain)
        self.message_id = msg_id
        self.sender = sender


class ReceivedGroupMessage(ReceivedMessage):
    def __init__(self, raw_msg, msg_id, sender, group_id):
        super().__init__(raw_msg, msg_id, sender)
        self.group_id = group_id
