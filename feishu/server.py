import sys
import asyncio
import logging
import requests
from sanic import Sanic, Blueprint
from sanic.log import logger

# Linux服务器上部署需要增加模块地址到PYTHONPATH
from consts import SYS_PATH
sys.path.append(SYS_PATH)

from apis import setup_event_blueprint
from consts import VERIFY_TOKEN, ENCRYPT_KEY, PATH_EVENT
from models import EventContent, Event
from client import FeishuClient


def create_sanic_server(verify_token: str = '', encrypt_key: str = '') -> Sanic:
    # 订阅事件(models.event)
    app = Sanic("feishu")

    async def on_event(event: [Event]):
        await asyncio.sleep(1)
        event_type = event.header.event_type
        logger.info(f"event_type: {event_type}")
        logger.info(f"event: {event}")
        if event_type == "im.message.receive_v1":
            async def send_message(event: [EventContent]):
                client = FeishuClient()
                receive_id = event.sender.sender_id.open_id
                text = f"""<at user_id="ou_1e20496774ba8483cdcb0cf8398296b0">TEST</at> {event.message}"""
                message_id = client.send_text(text, receive_id)
                print(f"message_id: {message_id}")
            await send_message(event.event)
        elif event_type == "im.message.reaction.created_v1":
            async def send_message(event: [EventContent]):
                client = FeishuClient()
                receive_id = event.user_id.open_id
                text = f"""<at user_id="ou_1e20496774ba8483cdcb0cf8398296b0">TEST</at> {event.reaction_type.emoji_type}"""
                message_id = client.send_text(text, receive_id)
                print(f"message_id: {message_id}")

            await send_message(event.event)

    event_app = Blueprint(name="event_app")
    setup_event_blueprint("sanic", blueprint=event_app, path=PATH_EVENT,
                          on_event=on_event, verify_token=verify_token, encrypt_key=encrypt_key)

    app.blueprint(event_app)
    logger.setLevel(logging.INFO)
    return app


def run_sanic_server(encrypt_key: str = ENCRYPT_KEY.strip(),
                     verify_token: str = VERIFY_TOKEN.strip()):
    app = create_sanic_server(encrypt_key=encrypt_key,
                              verify_token=verify_token)
    port = 9000
    host = requests.get("https://api.ipify.org/").text

    async def print_notice():
        logger.info("非局域网访问需要确保服务器有静态公网IP")
        logger.info(f"需要在飞书后台配置订阅信息URL = 'http://{host}:{port}{PATH_EVENT}'")

    app.add_task(print_notice())
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=port)


if __name__ == '__main__':
    run_sanic_server()
