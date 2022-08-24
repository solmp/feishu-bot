from typing import Tuple

from .base import BaseAPI, allow_async_call

__all__ = [
    'AuthAPI'
]


class AuthAPI(BaseAPI):

    @allow_async_call
    def get_app_access_token(self) -> Tuple[str, str, int]:
        """
        获取 app_access_token（企业自建应用）
        {
            "app_access_token": "x-xxx",
            "code": 0,
            "expire": 6864,
            "msg": "ok",
            "tenant_access_token": "y-yyy"
        }
        Returns:
            Tuple[app_access_token, tenant_access_token, expire]
        """
        api = "/auth/v3/app_access_token/internal"
        payload = {
            "app_id": self.client.app_id,
            "app_secret": self.client.app_secret,
        }

        result = self.client.request("POST", api=api, payload=payload, auth=False)

        return result["app_access_token"], result["tenant_access_token"], result["expire"]

    @allow_async_call
    def get_tenant_access_token(self) -> Tuple[str, int]:
        """获取自建应用的token
        https://open.feishu.cn/document/ukTMukTMukTM/uIjNz4iM2MjLyYzM
        Returns:
            Tuple[token, expire]
        """
        api = "/auth/v3/tenant_access_token/internal/"
        payload = {
            "app_id": self.client.app_id,
            "app_secret": self.client.app_secret,
        }

        result = self.client.request("POST", api=api, payload=payload, auth=False)
        # 返回 Body ：
        # {
        #     "code": 0,
        #     "expire": 7200,
        #     "msg": "ok",
        #     "tenant_access_token": "x-xxx"
        # }
        return result["tenant_access_token"], result["expire"]

    def resend_app_ticket(self):
        """重新推送app_ticket
        仅支持商店应用使用，不支持自建应用
        https://open.feishu.cn/document/ukTMukTMukTM/uQjNz4CN2MjL0YzM
        """
        raise NotImplementedError
        pass
