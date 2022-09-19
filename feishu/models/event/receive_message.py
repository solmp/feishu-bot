import json
from enum import Enum
from typing import Union, Optional
from pydantic import BaseModel

from .base import UserID, EventContent
from ..message.base import MessageType
from ..message.im.content import (TextContent, PostContent, ImageContent, InteractiveContent, ShareChatContent,
                                  ShareUserContent, AudioContent, MediaContent, FileContent, StickerContent)

__all__ = [
    'SenderType', 'ChatType',
    'Mentions', 'Sender', 'Message', 'ReceiveMessageEven', 'EmojiMessageEven'
]


class SenderType(str, Enum):
    USER = "user"


class ChatType(str, Enum):
    P2P = "p2p"
    GROUP = "group"


class Mentions(BaseModel):
    key: str
    id: UserID
    name: str
    tenant_key: str


class Sender(BaseModel):
    """
    {
        "sender_id": {
            "union_id": "on_8ed6aa67826108097d9ee143816345",
            "user_id": "e33ggbyz",
            "open_id": "ou_84aad35d084aa403a838cf73ee18467"
        },
        "sender_type": "user",
        "tenant_key": "736588c9260f175e"
    }
    """
    sender_id: UserID
    sender_type: SenderType
    tenant_key: str


class Message(BaseModel):
    """
    {
        "message_id": "om_5ce6d572455d361153b7cb51da133945",
        "root_id": "om_5ce6d572455d361153b7cb5xxfsdfsdfdsf",
        "parent_id": "om_5ce6d572455d361153b7cb5xxfsdfsdfdsf",
        "create_time": "1609073151345",
        "chat_id": "oc_5ce6d572455d361153b7xx51da133945",
        "chat_type": "group",
        "message_type": "text",
        "content": "{\"text\":\"@_user_1 hello\"}",
        "mentions": [
            {
                "key": "@_user_1",
                "id": {
                    "union_id": "on_8ed6aa67826108097d9ee143816345",
                    "user_id": "e33ggbyz",
                    "open_id": "ou_84aad35d084aa403a838cf73ee18467"
                },
                "name": "Tom",
                "tenant_key": "736588c9260f175e"
            }
        ]
    }
    """
    message_id: str
    message_type: MessageType
    content: Union[
        TextContent, PostContent, ImageContent, InteractiveContent, ShareChatContent,
        ShareUserContent, AudioContent, MediaContent, FileContent, StickerContent, dict, str
    ]
    root_id: Optional[str]
    parent_id: Optional[str]
    create_time: Optional[str]
    chat_id: Optional[str]
    chat_type: Optional[ChatType]
    mentions: Optional[Mentions]


class ReceiveMessageEven(EventContent):
    sender: Sender
    message: Message

    def __init__(self, **kwargs):
        content = kwargs['message']['content']
        if type(content) == str:
            kwargs['message']['content'] = json.loads(content)
        super(ReceiveMessageEven, self).__init__(**kwargs)


class ReactionType(BaseModel):
    emoji_type: str


class EmojiMessageEven(EventContent):
    message_id: str
    reaction_type: ReactionType
    operator_type: str
    user_id: UserID
    app_id: Optional[str]
    action_time: str
