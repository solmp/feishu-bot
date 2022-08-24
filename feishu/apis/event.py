"""订阅事件处理
包含订阅事件的sanic blueprint实现
"""
import asyncio
import json
import logging
from pydantic import ValidationError
from sanic import Blueprint, response
from sanic.request import Request
from typing import Optional, Callable, Awaitable, Union

from feishu.models import (Event, EventContent, EventType, ReceiveMessageEven)
from feishu.utils import decrypt, FeishuError, ERRORS

logger = logging.getLogger("feishu")

__all__ = ['setup_event_blueprint']


def setup_event_blueprint(framework: str, blueprint: Blueprint,
                          path: str, on_event: callable, verify_token: Optional[str] = None,
                          encrypt_key: Optional[str] = None):
    """配置一个用于接收订阅事件的Blueprint
    https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM
    Args:
        framework: sanic
        blueprint: sanic的Blueprint对象
        path: 回调路径, 只需包含blueprint后的挂载部分
        on_event:
            有订阅事件时, 接收Event的参数, 无需返回
            当framework="sanic"时, on_event函数会被asyncio.create_task添加，
                请确保asyncio的loop配置正确，e.g. set_default_loop, 或者注意运行的先后顺序
                一般情况下直接用sanic不应该出现任何问题
        verify_token: 校验token, 需和飞书后台配置一致, 不提供则不校验请求来源
        encrypt_key: 加密key, 需和飞书后台配置一致, 不提供则无法解析加密数据
    """
    if framework == "sanic":
        return sanic_blueprint(blueprint=blueprint, path=path, on_event=on_event,
                               verify_token=verify_token, encrypt_key=encrypt_key)
    else:
        raise NotImplementedError


def sanic_blueprint(blueprint: Blueprint, path: str,
                    on_event: Callable[[Event], Awaitable[None]],
                    verify_token: Optional[str] = None, encrypt_key: Optional[str] = None):
    """配置一个用于接收消息交互回调的sanic.blueprint
    Args:
        blueprint: sanic的Blueprint对象
        path: 回调路径, 只需包含blueprint后的挂载部分
        on_event: 有Action事件时, 接收Event类型的参数, 无需任何返回
            on_event函数会被asyncio.create_task添加，
            请确保asyncio的loop配置正确，e.g. set_default_loop, 或者注意运行的先后顺序
            一般情况下直接用sanic不应该出现任何问题
        verify_token: 校验token, 需和飞书后台配置一致, 不提供则不校验请求来源
        encrypt_key: 加密key, 需和飞书后台配置一致, 不提供则无法解析加密数据
    """

    @blueprint.route(path, methods=["POST"])
    async def handle_event(request: Request):
        payload: dict = request.json
        if "encrypt" in payload:
            payload = json.loads(decrypt(encrypt_key, payload["encrypt"]))

        # V1.0: url_verification, event_callback
        event_type = payload.get("type")
        if event_type == "url_verification":
            return url_verification(payload)
        elif event_type == "event_callback":
            event = Event(**payload)
            asyncio.create_task(on_event(event))
        elif payload.get('schema') == "2.0":
            # V2.0
            event = Event(**payload)
            event_type = event.header.event_type
            event.event = adapt_event(event_type, event.event)
            asyncio.create_task(on_event(event))
        else:
            raise NotImplementedError
        return response.json({})

    def url_verification(payload: dict):
        """配置请求网址后飞书会发送的验证请求
        https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM#%E9%85%8D%E7%BD%AE%E8%AF%B7%E6%B1%82%E7%BD%91%E5%9D%80
        """
        if verify_token and verify_token != payload.get("token"):
            return response.json(dict(challenge=""))
        return response.json(dict(challenge=payload.get("challenge")))


def adapt_event(event_type: [str], event: [EventContent]) -> Union[dict, EventContent]:
    """适配event的真实类型"""
    event_cls: Optional[EventContent] = {
        EventType.im_message_receive_v1: ReceiveMessageEven,
    }.get(event_type)

    if event_cls:
        try:
            return event_cls(**event)
        except ValidationError:
            raise FeishuError(ERRORS.VALIDATION_ERROR, f"解析事件失败，原始数据 event = {event}")
    else:
        # 不知道是啥类型，直接返回原始的dict
        return event
