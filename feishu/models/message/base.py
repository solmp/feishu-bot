from enum import Enum
from typing import Union
from pydantic import BaseModel

__all__ = [
    'MessageType', 'MessageContent', 'SendMessage', 'ReceiveIdType'
]


class MessageType(str, Enum):
    TEXT = "text"  # 文本
    POST = "post"  # 富文本
    IMAGE = "image"  # 图片
    INTERACTIVE = "interactive"  # 消息卡片
    SHARE_CHAT = "share_chat"  # 分享群名片
    SHARE_USER = "share_user"  # 分享个人名片
    AUDIO = "audio"  # 语音
    MEDIA = "media"  # 视频
    FILE = "file"  # 文件
    STICKER = "sticker"  # 表情包


class ReceiveIdType(str, Enum):
    OpenId = "open_id"
    UserId = "user_id"
    UnionId = "union_id"
    Email = "email"
    ChatId = "chat_id"


class MessageContent(BaseModel):
    pass


class SendMessage(BaseModel):
    """消息基类
    发送消息 content 说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json
    example:
    {
        "receive_id": "ou_7d8a6e6df7621556ce0d21922b676706ccs",
        "content": "{\"text\":\" test content\"}",
        "msg_type": "text"
    }

    :arg
    receive_id：依据receive_id_type(chat_id/open_id/user_id)的值，填写对应的消息接收者id，必填
    content 消息内容，json结构序列化后的字符串。不同msg_type对应不同内容，必填
    msg_type 消息类型 MessageType，必填
    """
    receive_id: str
    content: Union[MessageContent, str]
    msg_type: MessageType
