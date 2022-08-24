import asyncio
import hashlib
import inspect
import linecache
import logging
import os
import re
import secrets
import textwrap
from asyncio import AbstractEventLoop
from functools import wraps

__all__ = ['BaseAPI', 'allow_async_call', 'get_or_create_event_loop']


class BaseAPI:
    logger = logging.getLogger("feishu")

    def __init__(self, feishu_client: "FeishuClient"):
        self.client: feishu_client = None

    def adapt_sync_and_async(self, method, *args, **kwargs):
        pass


def verify_signature(verify_token: str, headers: dict, body: bytes) -> bool:
    """消息卡片安全校验
    https://open.feishu.cn/document/ukTMukTMukTM/uYzMxEjL2MTMx4iNzETM
    Args:
        verify_token: 飞书后台事件订阅中的Verification Token
        headers: 返回的HTTP Headers
        body: 返回的HTTP Body
    """
    timestamp = headers.get('X-Lark-Request-Timestamp')
    nonce = headers.get('X-Lark-Request-Nonce')
    encoded = (timestamp + nonce + verify_token).encode('utf-8')
    signature = hashlib.sha1(encoded + body).hexdigest()
    return headers['X-Lark-Signature'] == signature


def get_or_create_event_loop() -> AbstractEventLoop:
    try:
        loop = asyncio.get_event_loop()
        return loop
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


# ****************** @allow_async_call ******************
to_be_created = {}
context = {}
# name -> newname
# "= name(...)" -> "= await newname(...)"
async_method_mapping = {
    "self.client.request": "self.client.request",
    "self.client.fetch": "self.client.fetch"
}


def allow_async_call(func):
    """给同步方法加上被异步调用的能力

    为了让异步调用中不会被同步方法卡住event_loop
    加allow_async_call修饰的方法必须做到以下几点:

    - 方法中没有同步IO事件, 读写文件都最好不要有(本地磁盘且小文件问题不大)
    - API请求用self.client.request, 且一定要写成xxxx = self.client.request这样的形式
    - 通用HTTP请求用self.client.fetch, 且一定要携程yyyy = self.client.fetch这样的形式
    """

    global context, async_method_mapping, to_be_created
    name = func.__name__
    newname = name + "_async"
    async_method_mapping["self." + name] = "self." + newname

    def create_async_api(func=func, name=name):
        """生成async版本的API, 名字为原方法+'_async'

        Args:
            func: 同步版本的函数
            name: 同步版本的函数名
        """
        # 用正则生成一下async版本的代码
        # 注意，这个代码只在context中没有找到async代码时才会执行
        # 这里更好的方案是用ast，但是太麻烦了——正则大部分时候ok就行
        # def f(self, a):                             async f_async(self, a):
        #     ...                                         ...
        #     xxxx = self.client.request(...   =>         xxxx = await self.client.request(...
        #     yyyy = self.client.fetch(...     =>         yyyy = await self.client.fetch(...
        #     ...                                         ...
        source = inspect.getsource(func)
        source = textwrap.dedent(source)

        # 加上async def
        source2 = re.compile(r'def(\s*' + name + r')(\(.*?)->[^:]*:\s*\n\s{4}', re.DOTALL).sub(
            r'async def\1_async\2-> "Future":\n    ', source)
        if source2 == source:
            source2 = re.compile(r'def(\s*' + name + r')(\(.*?)\):\s*\n\s{4}', re.DOTALL).sub(
                r'async def\1_async\2) -> "Future":\n    ', source2)
        source = source2

        # 修改await, 目前就修改两种:
        # - xxx = self.method
        # - return self.method
        for method, newmethod in async_method_mapping.items():
            source = re.sub(r'\s{4}(\S+)\s*=\s*(' + re.escape(method) + r')(.*?\n*|\s{4})',
                            r'    \1 = await ' + newmethod + r'\3',
                            source)
            source = re.sub(r' (\s*)return\s*(' + re.escape(method) + r')(.*?\n*|\s{4})',
                            r' \1return await ' + newmethod + r'\3',
                            source)
        # 去掉decorator
        source = re.sub(r'\s*@allow_async_call\s*\n', '', source)

        # 试着从源文件import各种依赖，以免调用的时候出问题
        filename = func.__code__.co_filename[:-3].replace(os.path.sep, '.')
        paths = filename.split('.')
        for i in range(1, min(6, len(paths) + 1)):
            path = ".".join(paths[-i:])
            # if "." not in path:
            #     path = "." + path
            if "-" in path:
                break
            try:
                insert = f"from {path} import *\n"
                exec(insert)
            except:
                continue
            else:
                source = insert + source

                # 成功一次就应该够了
                break
        insert = "" \
                 "from typing import *\n" \
                 "from feishu import *\n" \
                 "from feishu.apis import *\n" \
                 "from feishu.client import *\n" \
                 "from feishu.models import *\n" \
                 "from feishu.utils import *\n" \
                 ""
        source = insert + source

        # 生成临时文件并预编译
        # 这个输出太多了暂时禁用
        # BaseAPI.logger.debug(f"自动生成的async版本API:{name} ---\n{source}")
        filename = "api_" + secrets.token_hex(4) + ".py"
        compiled = compile(source, filename, mode="exec")
        linecache.cache[filename] = (len(source), None, [line + '\n' for line in source.splitlines()], filename)
        exec(compiled, globals())

        context[newname] = globals()[newname]

    to_be_created[newname] = create_async_api

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        def create_async_apis():
            for newname2, create in to_be_created.items():
                create()
                setattr(self.__class__, newname2, context[newname2])

        if not hasattr(self.__class__, newname):
            create_async_apis()

        if not self.client.run_async or name == 'dummy':
            return func(self, *args, **kwargs)
        else:
            # print("calling", self, newname, "args", args, "kwargs", kwargs)
            if not self.client.event_loop or self.client.event_loop.is_closed():
                self.client.event_loop = get_or_create_event_loop()

            if not hasattr(self, newname):
                create_async_apis()

            return asyncio.ensure_future(
                getattr(self, newname)(*args, **kwargs),
                loop=self.client.event_loop
            )

    return wrapper
