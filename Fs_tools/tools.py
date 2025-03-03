import json
import requests
import lark_oapi as lark
from lark_oapi.api.contact.v3 import *


def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }
    params = {
        'app_id': 'cli_a74f9e0246b9d01c',
        'app_secret': '0r5DGzqFsv2bKc2uCv5CpAAQ6GcLnCbY',
    }
    response = requests.request("POST", headers=headers, url=url, params=params)
    return response.json()['tenant_access_token']


def get_open_id_by_lark(emails):
    # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a74f9e0246b9d01c") \
        .app_secret("0r5DGzqFsv2bKc2uCv5CpAAQ6GcLnCbY") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: BatchGetIdUserRequest = BatchGetIdUserRequest.builder() \
        .user_id_type("open_id") \
        .request_body(BatchGetIdUserRequestBody.builder()
                      .emails([emails])
                      .mobiles([])
                      .include_resigned(True)
                      .build()) \
        .build()

    # 发起请求
    response: BatchGetIdUserResponse = client.contact.v3.user.batch_get_id(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.contact.v3.user.batch_get_id failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return response.data["user_list"]["email"]


def getOpenID(email):
    params = {
        "emails": [email],
    }
    Authorization = get_token()
    headers = {
        'Authorization': 'Bearer %s' % Authorization,
        'Content-Type': 'application/json; charset=utf-8'
    }
    url = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
    response = requests.request("POST", url=url, data=json.dumps(params), headers=headers)
    if response.json()["code"] == 0:
        print(response.json())
        return response.json()["data"]["user_list"][0]["user_id"]
    else:
        return 0


open_id = getOpenID("wangqicong@papegames.net")
print(open_id)