import asyncio

from feishu.client import FeishuClient

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = FeishuClient(run_async=False)
client_async = FeishuClient(run_async=True)


def test_tenant_access_token():
    token, expire = client.get_tenant_access_token()
    assert token and expire > 0
    print(f" token: {token}, expire: {expire}")

    assert token and expire

    token, expire = loop.run_until_complete(client_async.get_tenant_access_token())
    assert token and expire > 0
    print(f" token: {token}, expire: {expire}")


if __name__ == "__main__":
    test_tenant_access_token()
