# feishu_bot

> 飞书群聊机器人

## models

> 各种事件、消息格式、类型
> event、message

### event: 订阅事件格式

- [x] base: Event, EventContent, EventType
- [x] ReceiveMessageEven: 接收10种消息事件详细格式

### message: 消息格式

- [x] im：10种消息发送格式

> TextMessage, PostMessage, ImageMessage, InteractiveMessage, ShareChatMessage,
> ShareUserMessage, AudioMessage, MediaMessage, FileMessage, StickerMessage,

- [x] base: SendMessage, MessageContent, MessageType, ReceiveIdType

## utils

> 工具

- [x] AES: 飞书数据解密
- [x] errors: 异常处理、错误代码

## apis

> 提供各种功能接口

- base
    - [x] verify_signature: 安全校验
    - [x] allow_async_call：异步调用注解
- [x] feishu_api: 飞书API基类
- event: 订阅事件监听处理
    - [x] 接收消息
- [x] auth(获取API访问凭证)：app_access_token, tenant_access_token
- [x] message: 发送消息API

## client

> 客户端：发送请求、消息

- [x] base
- [x] client: 同步/异步请求封装（json: requests; 字节流: fetch）

## server

> 服务端：订阅事件

- [x] 接收消息事件
-

## 其它

- consts：配置常量
    - base_url：飞书开放平台服务端 API 的 URL
    - PATH_EVENT：事件订阅请求网址
    - APP_ID, APP_SECRET, VERIFY_TOKEN, ENCRYPT_KEY
    - TOKEN_EXPIRE_TIME, TOKEN_UPDATE_TIME, BATCH_SEND_SIZE
- stores：持久化
    - 内存：MemoryStore
    - Redis：RedisStore



