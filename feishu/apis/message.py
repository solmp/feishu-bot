"""消息管理相关API
- 发送文本、富文本、图片、消息卡片
- 分享群名片、个人名片
- 发送语音、视频、文件、表情包
"""
import json
from typing import Optional, Union

from .base import BaseAPI, allow_async_call
from feishu.models import (SendMessage, MessageType, MessageContent, ReceiveIdType,
                           TextMessage, PostMessage, ImageMessage, InteractiveMessage, ShareChatMessage,
                           ShareUserMessage, AudioMessage, MediaMessage, FileMessage, StickerMessage,
                           TextContent, PostContent, ImageContent, InteractiveContent, ShareChatContent,
                           ShareUserContent, AudioContent, MediaContent, FileContent, StickerContent)

__all__ = ['MessageAPI']


def create_message(msg_type: MessageType, content: MessageContent, receive_id: str) -> SendMessage:
    message_cls = {
        MessageType.TEXT: TextMessage,
        MessageType.POST: PostMessage,
        MessageType.IMAGE: ImageMessage,
        MessageType.INTERACTIVE: InteractiveMessage,
        MessageType.SHARE_CHAT: ShareChatMessage,
        MessageType.SHARE_USER: ShareUserMessage,
        MessageType.AUDIO: AudioMessage,
        MessageType.MEDIA: MediaMessage,
        MessageType.FILE: FileMessage,
        MessageType.STICKER: StickerMessage,
    }[msg_type]

    msg = message_cls(
        receive_id=receive_id,
        msg_type=msg_type,
        content=content
    )
    return msg


class MessageAPI(BaseAPI):
    """消息管理相关API
    https://open.feishu.cn/document/ukTMukTMukTM/uUjNz4SN2MjL1YzM
    """

    @allow_async_call
    def send(self, message: Union[SendMessage, dict], receive_id_type: ReceiveIdType) -> Optional[str]:
        """发送/im/v1/messages请求, 返回message_id
        Args:
            message: Message类型或者一个简单的dict
            receive_id_type: 消息接收者id类型
        Returns:
            str: message_id
        Usages::
        >>> from feishu.models import MessageType, SendMessage, TextContent, ReceiveIdType
        >>> from feishu.client import FeishuClient
        >>> msg = SendMessage(receive_id="xxx", msg_type=MessageType.TEXT, content=TextContent(text="xxx"))
        >>> # or
        >>> # msg = msg = {"receive_id": receive_id, "msg_type": MessageType.TEXT, "content": {"text": "xxx"}}
        >>>
        >>> client = FeishuClient(...)
        >>> message_id = client.send(msg, ReceiveIdType.OpenId)
        >>> client.send(msg)
        """
        api = "/im/v1/messages"
        if isinstance(message, SendMessage):
            payload = message.dict(exclude_none=True)
        else:
            payload = message
        # content json序列化
        payload['content'] = json.dumps(payload['content'])

        param = {'receive_id_type': receive_id_type}
        result = self.client.request("POST", api=api, payload=payload, params=param)
        return result.get("data", {}).get("message_id")

    @allow_async_call
    def send_text(self, text: str, receive_id: str,
                  receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送文本
        Args:
            text: 待发送的文本
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        msg = create_message(MessageType.TEXT, content=TextContent(text=text), receive_id=receive_id)
        if text.strip():
            return self.send(msg, receive_id_type)
        else:
            self.logger.warning(f"text为空, 文本未发送: msg={msg}")

    @allow_async_call
    def send_post(self, post: Union[PostContent, dict], receive_id: str,
                  receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送富文本
        Args:
            post: 待发送的富文本
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        msg = create_message(MessageType.POST, content=PostContent(**post), receive_id=receive_id)
        if post:
            return self.send(msg, receive_id_type)
        else:
            self.logger.warning(f"post为空, 富文本未发送: msg={msg}")

    @allow_async_call
    def send_image(self, image_key: str, receive_id: str,
                   receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送图片
        Args:
            image_key: 待发送的图片
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        msg = create_message(MessageType.IMAGE, content=ImageContent(image_key=image_key), receive_id=receive_id)
        if image_key.strip():
            return self.send(msg, receive_id_type)
        else:
            self.logger.warning(f"image为空, 图片未发送: image_key={image_key}")

    @allow_async_call
    def send_interactive(self, interactive: str, receive_id: str,
                         receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送消息卡片 TODO
        Args:
            interactive: 待发送的消息卡片
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        raise NotImplementedError
        # msg = create_message(MessageType.INTERACTIVE, INTERACTIVEtent=InteractiveContent(), receive_id=receive_id)
        # if interactive.strip():
        #     return self.send(msg, receive_id_type)
        # else:
        #     self.logger.warning(f"interactive为空, 消息卡片未发送: msg={msg}")

    @allow_async_call
    def send_share_chat(self, chat_id: str, receive_id: str,
                        receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送分享群名片
        Args:
            chat_id: 待发送的群名片ID
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        msg = create_message(MessageType.SHARE_CHAT, content=ShareChatContent(chat_id=chat_id), receive_id=receive_id)
        if chat_id.strip():
            return self.send(msg, receive_id_type)
        else:
            self.logger.warning(f"chat_id为空, 群名片未发送: chat_id={chat_id}")

    @allow_async_call
    def send_share_user(self, user_id: str, receive_id: str,
                        receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送分享个人名片
        Args:
            user_id: 待发送的个人名片ID
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        msg = create_message(MessageType.SHARE_USER, content=ShareUserContent(user_id=user_id), receive_id=receive_id)
        if user_id.strip():
            return self.send(msg, receive_id_type)
        else:
            self.logger.warning(f"user_id为空, 个人名片未发送: user_id={user_id}")

    @allow_async_call
    def send_audio(self, audio_file_key: str, receive_id: str,
                   receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送语音
        Args:
            audio_file_key: 待发送的语音
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        msg = create_message(MessageType.AUDIO, content=AudioContent(file_key=audio_file_key), receive_id=receive_id)
        if audio_file_key.strip():
            return self.send(msg, receive_id_type)
        else:
            self.logger.warning(f"audio_file_key为空, 语音未发送: audio_file_key={audio_file_key}")

    @allow_async_call
    def send_media(self, media_file_key: str, media_image_key: Optional[str], receive_id: str,
                   receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送视频
        Args:
            media_file_key:    文件key
            media_image_key:   视频封面图片key
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        media = MediaContent(file_key=media_file_key, image_key=media_image_key)
        msg = create_message(MessageType.MEDIA, content=media, receive_id=receive_id)
        if media_file_key.strip():
            return self.send(msg, receive_id_type)
        else:
            self.logger.warning(f"media为空, 视频未发送: media_file_key={media_file_key}, media_image_key={media_image_key}")

    @allow_async_call
    def send_file(self, file_key: str, receive_id: str,
                  receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送文件
        Args:
            file_key: 待发送的文件
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        msg = create_message(MessageType.FILE, content=FileContent(file_key=file_key), receive_id=receive_id)
        if file_key.strip():
            return self.send(msg, receive_id_type)
        else:
            self.logger.warning(f"file为空, 文件未发送: file_key={file_key}")

    @allow_async_call
    def send_sticker(self, sticker_file_key: str, receive_id: str,
                     receive_id_type: ReceiveIdType = ReceiveIdType.OpenId) -> Optional[str]:
        """发送表情包
        Args:
            sticker_file_key: 待发送的表情包
            receive_id_type: 消息接收者id类型
            receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        """
        msg = create_message(MessageType.STICKER, content=StickerContent(file_key=sticker_file_key),
                             receive_id=receive_id)
        if sticker_file_key.strip():
            return self.send(msg, receive_id_type)
        else:
            self.logger.warning(f"sticker_file_key为空, 表情包未发送: sticker_file_key={sticker_file_key}")
