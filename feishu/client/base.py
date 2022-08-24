import logging
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from enum import Enum
from typing import Union

__all__ = [
    'FeishuBaseClient', 'AppType'
]


class AppType(str, Enum):
    TENANT = "tenant"  # 企业自建应用
    USER = "user"  # 第三方应用


class FeishuBaseClient(ABC):
    logger = logging.getLogger("feishu")

    app_id: str
    app_secret: str
    run_async: bool
    event_loop: AbstractEventLoop

    @abstractmethod
    def request(self, method: str, api: str, params: dict = {}, payload: dict = {},
                data: dict = {}, files: dict = {}, auth: str = True) -> Union[dict, bytes]:
        """发起请求
        Args:
            method: "GET" or "POST"
            api: 对应功能的API Path, e.g. "/im/v1/messages"
            params: HTTP的URL参数
            payload: Body的参数, 会序列化为json
            data: form-data
            files: multipart/form-data
            auth: 是否需要验证, 只有token类API需要设为False

        Returns:
            一个解析好的返回dict，为飞书的标准格式
            code: 0为正常
            msg:  出错信息
            data: 数据信息

        Raises:
            FeishuException
        """
        pass
