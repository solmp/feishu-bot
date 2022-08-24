import config

base_url = "https://open.feishu.cn/open-apis"
# PATH_EVENT = "/feishu/event"

# APP_ID = "cli_a38a41bc1039d00e"
# APP_SECRET = "oZAax5g9NrSWviUSzJA4qxTj428NivM6"
# VERIFY_TOKEN = "j8SkDHJtG8CVO9uMC2tovchuf2AaWsBn"
# ENCRYPT_KEY = "nZbv97wut5iOs8STK8PYsAZbEzjNyrdD"

PATH_EVENT = config.PATH_EVENT
APP_ID = config.APP_ID
APP_SECRET = config.APP_SECRET
VERIFY_TOKEN = config.VERIFY_TOKEN
ENCRYPT_KEY = config.ENCRYPT_KEY

TOKEN_EXPIRE_TIME = 7200  # token时效
TOKEN_UPDATE_TIME = 1800  # token提前更新的时间
BATCH_SEND_SIZE = 200  # 批量发送消息列表的大小限制
