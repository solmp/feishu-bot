from ..base import SendMessage, MessageType
from .content import (TextContent, PostContent, ImageContent, InteractiveContent, ShareChatContent,
                      ShareUserContent, AudioContent, MediaContent, FileContent, StickerContent)

__all__ = [
    "TextMessage", "PostMessage", "ImageMessage", "InteractiveMessage", "ShareChatMessage",
    "ShareUserMessage", "AudioMessage", "MediaMessage", "FileMessage", "StickerMessage",
]


class TextMessage(SendMessage):
    """文本
    {
        "text": "test content"
    }
    """
    msg_type: MessageType = MessageType.TEXT
    content: TextContent


class PostMessage(SendMessage):
    """富文本
    {
        "zh_cn": {
            "title": "我是一个标题",
            "content": [
                [{
                        "tag": "text",
                        "text": "第一行 :"
                    },
                    {
                        "tag": "a",
                        "href": "http://www.feishu.cn",
                        "text": "超链接"
                    },
                    {
                        "tag": "at",
                        "user_id": "ou_1avnmsbv3k45jnk34j5",
                        "user_name": "tom"
                    }
                ],
                [{
                    "tag": "img",
                    "image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"
                }],
                [{
                        "tag": "text",
                        "text": "第二行:"
                    },
                    {
                        "tag": "text",
                        "text": "文本测试"
                    }
                ],
                [{
                    "tag": "img",
                    "image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"
                }]
            ]
        },
        "en_us": {
            ...
        }
    }
    """
    msg_type: MessageType = MessageType.POST
    content: PostContent


class ImageMessage(SendMessage):
    """图片
    {
        "image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"
    }
    """
    msg_type: MessageType = MessageType.IMAGE
    content: ImageContent


class InteractiveMessage(SendMessage):
    """消息卡片
    卡片结构各字段说明请参考[卡片模块介绍](https://open.feishu.cn/document/ukTMukTMukTM/uMjNwUjLzYDM14yM2ATN) 。
    还可以使用 [消息卡片搭建工具](https://open.feishu.cn/tool/cardbuilder)自由搭建你需要的卡片。
    {
        "receive_id": "oc_820faa21d7ed275b53d1727a0feaa917",
        "content": "...",
        "msg_type": "interactive"
    }
    """
    msg_type: MessageType = MessageType.INTERACTIVE
    content: InteractiveContent


class ShareChatMessage(SendMessage):
    """分享群名片
    {
        "chat_id": "oc_0dd200d32fda15216d2c2ef1ddb32f76"
    }
    """
    msg_type: MessageType = MessageType.SHARE_CHAT
    content: ShareChatContent


class ShareUserMessage(SendMessage):
    """分享个人名片
    {
        "user_id": "ou_0dd200d32fda15216d2c2ef1ddb32f76"
    }
    """
    msg_type: MessageType = MessageType.SHARE_USER
    content: ShareUserContent


class AudioMessage(SendMessage):
    """语音
    {
        "file_key": "75235e0c-4f92-430a-a99b-8446610223cg"     //文件key
    }
    """
    msg_type: MessageType = MessageType.AUDIO
    content: AudioContent


class MediaMessage(SendMessage):
    """视频
    {
        "file_key": "75235e0c-4f92-430a-a99b-8446610223cg", //文件key
        "image_key": "img_xxxxxx"  // 视频封面图片key
    }
    """
    msg_type: MessageType = MessageType.MEDIA
    content: MediaContent


class FileMessage(SendMessage):
    """文件
    {
        "file_key": "75235e0c-4f92-430a-a99b-8446610223cg"
    }
    """
    msg_type: MessageType = MessageType.FILE
    content: FileContent


class StickerMessage(SendMessage):
    """表情包
    {
        "file_key": "75235e0c-4f92-430a-a99b-8446610223cg"
    }
    """
    msg_type: MessageType = MessageType.STICKER
    content: StickerContent
