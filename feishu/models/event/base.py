from enum import Enum
from typing import Union
from pydantic import BaseModel, Field

__all__ = [
    'EventType', 'EventContent', 'Event',
    'Header', 'UserID'
]


class EventType(str, Enum):
    MESSAGE = "message"
    im_message_receive_v1 = "im.message.receive_v1"


class EventContent(BaseModel):
    pass


class Header(BaseModel):
    event_id: str
    token: str
    create_time: str
    event_type: Union[str, EventType]
    tenant_key: str
    app_id: str


class Event(BaseModel):
    """目前响应事件数据格式 2.0
     {
        "schema": "2.0", // 事件格式的版本。无此字段的即为1.0
        "header": {
            "event_id": "f7984f25108f8137722bb63cee927e66",  // 事件的唯一标识
            "token": "066zT6pS4QCbgj5Do145GfDbbagCHGgF", // 即Verification Token
            "create_time": "1603977298000000", //  事件发送的时间
            "event_type": "contact.user_group.created_v3", // 事件类型
            "tenant_key": "xxxxxxx",  // 企业标识
            "app_id": "cli_xxxxxxxx", // 应用ID
        },
        "event":{
            ... // 不同事件此处数据不同
        }
    }
    """
    _schema: Field(alias="schema")
    header: Header
    event: Union[dict, EventContent]


# ********************** Public Type ********************** #


# ********************** Public Model ********************** #
class UserID(BaseModel):
    union_id: str
    user_id: str
    open_id: str
