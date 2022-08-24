from enum import Enum
from typing import Optional, List, Union
from pydantic import BaseModel

from ..base import MessageContent

__all__ = [
    "TextContent", "PostContent", "ImageContent", "InteractiveContent", "ShareChatContent",
    "ShareUserContent", "AudioContent", "MediaContent", "FileContent", "StickerContent",
]


class TextContent(MessageContent):
    text: str


class PostContent(MessageContent):
    class Post(BaseModel):
        # 国际化
        class I18nPost(BaseModel):
            class PostElement(BaseModel):
                class PostTag(str, Enum):
                    TEXT = "text"
                    A = "a"
                    AT = "at"
                    IMG = "img"

                tag: PostTag
                # text: text, un_escape
                # a: text, href
                # at: user_id, user_name
                # img: image_key
                text: Optional[str] = None
                un_escape: Optional[bool] = None

                href: Optional[str] = None

                user_id: Optional[str] = None
                user_name: Optional[str] = None

                image_key: Optional[str] = None

            title: Optional[str] = None
            content: List[List[PostElement]]

        zh_cn: Optional[Union[I18nPost, dict]] = None
        en_us: Optional[Union[I18nPost, dict]] = None
        # ...

    post: Post


class ImageContent(MessageContent):
    image_key: str


class InteractiveContent(MessageContent):
    """
    卡片结构各字段说明请参考[卡片模块介绍](https://open.feishu.cn/document/ukTMukTMukTM/uMjNwUjLzYDM14yM2ATN) 。
    还可以使用 [消息卡片搭建工具](https://open.feishu.cn/tool/cardbuilder)自由搭建你需要的卡片。
    """
    interactive: dict


class ShareChatContent(MessageContent):
    chat_id: str


class ShareUserContent(MessageContent):
    user_id: str


class AudioContent(MessageContent):
    # 通过[上传文件]接口获取音频文件 file_key。
    # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create
    file_key: str


class MediaContent(MessageContent):
    """
    file_key    文件key
    image_key   视频封面图片key
    """
    file_key: str
    image_key: Optional[str]


class FileContent(MessageContent):
    # 通过[上传文件]接口获取文件 file_key。
    # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create
    file_key: str


class StickerContent(MessageContent):
    # 目前仅支持发送机器人收到的表情包，
    # 可通过[接收消息事件]的推送获取表情包 file_key。
    # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive
    file_key: str
