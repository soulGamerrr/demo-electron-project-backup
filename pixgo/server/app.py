import json
import sys
#
sys.path.append("/home/demo-project")

from flask import Flask, request
from flask_cors import CORS
from pixivgo.pixgo.interface import PixivIllusts, PixivIllustCommend, PixivHome
from pixivgo.pixgo.userInterface import UserLogin
# from pixgo.interface import Illusts, IllustCommend
# from pixgo.userInterface import UserLogin

app = Flask(__name__)


CORS(app, supports_credentials=True)
CORS(app, resources=r'/*')


def get_json_info():
    '''

    :return: dict {"dataName": "dataInfo"}
    返回 由前端传来的数据，如果是 ‘POST’ 如下, 如果是 ‘GET’(待完善)
    '''

    return json.loads(request.get_data())



@app.route("/", methods=['GET', "POST"])
def home():
    print(request.base_url)
    return "Hello"


@app.route("/download", methods=['POST'])
def _download():


    info = json.loads(request.get_data())
    if info['urlOriginal'] != "":
        return {"error": True, "message": "not a real urlOriginal"}
    else:
        byteInfo = _download(info['urlOriginal'])
        return byteInfo


@app.route("/getInfo", methods=["POST"])
def _illust():
    # print(request.base_url)
    # print(request.get_json())

    resInfo = get_json_info()
    if resInfo['illustId'] == "":
        return {"error": True, "message": "Invalid {} or can not read this illustid".format(resInfo['illustId'])}

    # print("图片ID：", resInfo['illustId'])
    # 使用代理的方式为用户进行设置
    # 这里传入一个是否代理的值，后期添加 +++++++++++++++++++
    img_info, headers, url_proxy = PixivIllusts(resInfo['illustId'])._illust(isProxy=True)

    return {"error": False, "result": 200, "data": {
        "info": img_info,
        "url": url_proxy
        }
    }


@app.route("/commend", methods=['POST'])
def recommend():
    resInfo = get_json_info()
    if resInfo['illustId'] == "":
        return {"error": True, "message": "Invalid {} or can not read this illustid".format(resInfo['illustId'])}

    res, urlList, nextids = PixivIllustCommend(resInfo['illustId']).getImageCommend(resInfo['cookie'])
    return {"error": False,
        "result": 200, "response": res, "urlList": urlList, "nextIds": nextids
    }

@app.route("/login", methods=['POST'])
def _login():

    data_info = get_json_info()
    # 对于初次登录没有cookie参数的情况
    print(data_info)
    if data_info['cookie'] == "":
        result_info = UserLogin()._login(data_info['username'], data_info['password'])
        # print(result_info)
        if result_info["is_logged_in"] == True:
            return result_info
        else:
            return result_info
    else:
        check_result = UserLogin()._check_is_logged(data_info['cookie'])
        if check_result['result'] == 200:
            return check_result

    # if data_info['cookie'] == "":
    #     if data_info["username"] == "123" and data_info['password'] == "123":
    #         return {'result': 200, "cookie": "this is cookie", "is_logged_in": True}
    #     else:
    #         return {"result": 100}
    #
    # else:
    #     if data_info['cookie'] == "this is cookie":
    #         return {'result': 200, "is_logged_in": True}


@app.route("/illust_more", methods=['POST'])
def recommend_illust_more():
    """
    postInfo:   page_num => int
            page_size => int
            nextIds => list
    :return:
    """
    proxy_url = "https://i.pixiv.cat"

    data_info = get_json_info()
    page_num = data_info['page_num']
    page_size = data_info['page_size']
    ids = data_info['nextIds']
    response = PixivIllustCommend().loadMoreCommend(page_num=page_num, page_size=page_size, nextIds=ids)
    # print(response)
    illusts = response['body']['illusts']

    # 重新组装 url 使用代理的模式,以及不使用代理的模式
    for i in illusts:
        # print(type(i['url']))
        # print(illusts.index(i))
        if i.get('isAdContainer') == True:
            illusts.pop(illusts.index(i))
            continue
        else:
            i['url'] = proxy_url + i['url'][len(proxy_url):]
    return {'result': 200, "illusts": illusts}


@app.route("/home_page", methods=['POST'])
def home_page_info():

    data_info = get_json_info()
    # print(data_info)
    response = PixivHome().homePage(cookie=data_info['cookie'])
    # print(response)
    return response


@app.route("/rank", methods=['POST'])
def rank():

    data_info = get_json_info()
    # print(data_info)
    response = PixivHome().rank(mode=data_info['mode'])
    # print(response)
    return response

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
