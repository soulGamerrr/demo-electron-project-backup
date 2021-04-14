import base64
import json
import pickle
import time
import sys
import threading
import gevent
from typing import List

sys.path.append("pixgo")

from threading import Thread
from .parsing import *


class PixivDefault(object):
    """
    :param illustUrl -> str针对访问的时候添加referer请求源。
    :param illustDetail -> str单张图片的详细信息链接
    :param illustRank 插画排行榜链接
    :param bookMark -> str暂未定义
    :param dailyRecommend -> str每日推荐作品
    :param relativeRecommend -> str单张图片的相关推荐
    :param recommendMore -> str单张图片相关推荐获取更多的图片
    :param recommendParams -> dict 获取更多图片的相关参数
    :param headers 发送请求链接使用请求头
    """

    illustHome = "https://www.pixiv.net/ajax/top/{}?mode={}&lang=zh"
    illustUrl = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}"
    illustDetail = "https://www.pixiv.net/ajax/illust/"
    illustRank = "https://www.pixiv.net/ranking.php?mode={}&p={}&format=json"
    bookMark = None
    dailyRecommend = None
    relativeRecommend = "https://www.pixiv.net/ajax/illust/{}/recommend/init?"
    recommendMore = "https://www.pixiv.net/ajax/illust/recommend/illusts?"
    userInfoUrl = "https://www.pixiv.net/ajax/user/{}?full=1&lang=zh"
    userIllustsInfo = "https://www.pixiv.net/ajax/user/{}/profile/top?lang=zh"
    recommendParams = {
        "limit": 20,
        "lang": "zh"
    }
    headers = default_setting.DEFAULT_HEADER_HANDLER

    # 仅限图片代理，并不会访问pixiv
    imgUrlProxy = "https://i.pixiv.cat"
    # https://i.pixiv.cat/c/540x540_70/img-master/img/2021/01/24/02/53/01/87254574_p0_master1200.jpg'

# 首页排行，推荐用户，每日推荐
class PixivHome(PixivDefault):

    def __init__(self):
        super().__init__()

    @property
    def _session(self):
        return new_session()

    # 首页请求接口，返回为字典类型
    def homePage(self, cookie: str, type: str = default_setting.DEFAULT_TYPE, mode: str = default_setting.DEFAULT_MODE, isProxy=True) -> dict:

        default_type = {
            "illust": "illust",
            "manga": "manga",
            "novel": "novel",
        }

        default_mode = {
            "all": "all",
            "r18": "r18"
        }
        session = self._session
        session.headers['Cookie'] = cookie
        use_type = default_type[type]  # 由配置或前端传来的参数决定
        use_mode = default_mode[mode]  # 由配置或前端传来的参数决定
        start = time.time()
        response = req(url=self.illustHome.format(use_type, use_mode), session=session).json()
        body = response['body']
        # print(body)
        rank_list = self.home_rank_info(body)



        # 获取推荐用户的简要信息

        more_illusts = []
        num_of_users = len(body['page']['recommendUser'])
        for i in range(num_of_users):
            illustIds = body['page']['recommendUser'][i]["illustIds"]
            more_illusts.extend(illustIds)

        # 方法2: 直接调用 loadMore 的方法
        # 完成推荐用户的数据整合
        response_recommend_user_list_info = self.loadMore_ids(more_illusts, "recommendUser")['response']
        # 完成首页排行榜数据
        response_rank_list_info = self.loadMore_ids(rank_list, "rank")['response']
        # 加载首页每日推荐数据, 每次刷新就会重新加载新的推荐内容，或单独做成推荐列表展示
        response_recommend_list_info = self.loadMore_ids(body['page']['recommend']['ids'], "recommend")['response']

        # 方法1(保留).使用协程的方式同时对这个方法进行调用  运行时间 2.3025234234s  大约2s左右完成调用

        # g_list = gevent.joinall([gevent.spawn(self.loadMore_ids, rank_list, "rank"),
        #                 gevent.spawn(self.loadMore_ids, body['page']['recommend']['ids'], "recommend"),
        #                 gevent.spawn(self.loadMore_ids, more_illusts, "recommendUser")])
        # print(response_recommend_list_info, response_rank_list_info, response_recommend_user_list_info)
        # for i in g_list:
        #     # print(i)
        #     print("请求结果", i.value)

        end = time.time()
        print("总计用时 %s" % (end - start))

        # ************************************** 以上为方法 1 ********************************************* #

        # 对recommend_user_list_info进行数据处理
        
        recommend_user = self.get_user_info(response_recommend_user_list_info, self.imgUrlProxy)


        if isProxy:
            # ----------------------------------------------暂时注释 ---------------------------------------------------
            rank_illusts = self.proxyUrl(response_rank_list_info, self.imgUrlProxy)
            recommend_illusts = self.proxyUrl(response_recommend_list_info, self.imgUrlProxy)

            return {"result": 200, "rank": rank_illusts, "recommend": recommend_illusts, "items": body,
                    "recommend_user": recommend_user}
            # return {"result": 200, "recommend_user": recommend_user}
        else:
            pass

    def rank(self, mode: str, date: str = None, p: int = 1) -> dict:

        default_mode = {
            "daily": "daily",  # 每日
            "weekly": "weekly",  # 每周
            "monthly": "monthly",  # 每月
            "rookie": "rookie",  # 新人
            "male": "male",  # 男性向
            "female": "female",  # 女性向
            "daily_r18": "daily_r18",  # 每日xxx
            "weekly_r18": "weekly_r18",  # 每周xxx
            "male_r18": "male_r18",  # 男性向xxx
            "female_r18": "female_r18"  # 女性向xxx
        }

        session = self._session
        use_mode = default_mode[mode]
        response = req(url=self.illustRank.format(use_mode, p), session=session).json()
        print(response)
        return response


    # 对首页排行进行数据处理
    @staticmethod
    def home_rank_info(body):
        rank = body['page']['ranking']
        today_rank = rank['date']
        ranking_list = rank['items']
        rank_ids_lsit = []
        for item in ranking_list:
            rank_ids_lsit.append(item['id'])
        # print(rank_ids_lsit)
        return rank_ids_lsit

    # 按照插画的id进行更多的加载方式
    @staticmethod
    def loadMore_ids(rank_list: list, type:str):
        payload = {
            "illust_ids[]": []
        }
        url = "https://www.pixiv.net/ajax/illust/recommend/illusts?"
        payload['illust_ids[]'].append(rank_list)
        response = req(url=url, params=payload).json()
        return {"response": response, "request_type": type}



    # 使用代理链接替换原图片链接
    @staticmethod
    def proxyUrl(load_more, proxy_url):
        illusts = load_more['body']['illusts']

        for i in illusts:

            if i.get('isAdContainer') == True:
                illusts.pop(illusts.index(i))
                continue
            else:
                i['url'] = proxy_url + i['url'][len(proxy_url):]
                i['profileImageUrl'] = proxy_url + i['profileImageUrl'][len(proxy_url):]
        for i in illusts:
            if i.get('url')[:len(proxy_url)] == "https://i.pximg.net":
                illusts.pop(illusts.index(i))
        return illusts

    @staticmethod
    def get_user_info(resp: dict, proxy_url):

        user_data = {
            "userId": "",
            "illusts": []
        }

        user_data_list = list()
        user_id_list = []
        body = resp['body']['illusts']

        for id in body:
            if id.get("isAdContainer") == True:
                resp['body']['illusts'].pop(resp['body']['illusts'].index(id))
                continue
            # print(id.get('userId'))
            if id.get('userId') in user_id_list:
                continue
            else:
                user_id_list.append(id['userId'])
        for i in body:
            if i.get("isAdContainer") == True:
                resp['body']['illusts'].pop(resp['body']['illusts'].index(i))
                continue
            else:

                i['url'] = proxy_url + i['url'][len(proxy_url):]
                if re.search(r"user-profile", i['profileImageUrl']) == None:
                    continue
                i['profileImageUrl'] = proxy_url + i['profileImageUrl'][len(proxy_url):]

                i["profileImageUrl"] = i['profileImageUrl'].replace("_50.", "_170.")

        return {"userIdList": user_id_list, "body": body}



# 插画查看以及下载
class PixivIllusts(PixivDefault):

    def __init__(self, mid=""):

        self.illustId = mid
        self.url = self.illustDetail + self.illustId
        # self.urlSmall = self.illustUrl.format(mid)
        # self.headers["Referer"] = self.illustUrl.format(mid)
        # self._session = new_session()

        try:
            assert mid is not ""
        except AssertionError as e:
            # logged.log("错误信息: %s" % e, level=settings.LOG_ERROR)
            print(e)


    @property
    def _session(self):
        return new_session()

    # 根据图片ID获取图片的信息进行返回
    def _illust(self, log=False, isProxy=False):

        # print(self.url)
        session = self._session
        session.headers = self.headers
        res = req(url=self.url, session=session)
        self.imgInfo = getJson(res)
        urlSmall = self.imgInfo["small"]
        # 是否使用代理, 代理的图床可以不适用梯子进行访问，如果网络不允许，则无法访问。使用代理可以
        # 绕过主机进行访问。
        if isProxy:
            urlProxy = self.imgUrlProxy + urlSmall[len(self.imgUrlProxy):]
            # print(urlProxy)
            return self.imgInfo, self.headers, urlProxy
        else:
            pic_suffix = urlSmall.split(".")[-1]
            # 加载需要下载的图片
            byteInfo = req(urlSmall, headers=self.headers)
            # if log:
            #     logged = Logger("illust.log")
            #     logged.log("请求链接: %s " % self.url)

            # 将下载的图片二进制(byteInfo.content) 解码(decode) 然后编码转为base64格式
            base_data = base64.encodebytes(byteInfo.content).decode("utf-8")
            return self.imgInfo, self.headers, 'data:image/{};base64,%s'.format(pic_suffix) % base_data

    def getIllustInfo(self):
        res = req(self.url, headers=self.headers)
        self.imgInfo = getJson(res)
        return self.imgInfo

    def downloadIllust(self, origin):
        byteInfo = req(origin, headers=self.headers).content
        return byteInfo



class PixivIllustCommend(PixivDefault):

    def __init__(self, mid=""):

        self.illustId = mid
        self.url = self.illustDetail + self.illustId
        self.pid = None
        self.title = None
        self.pic_url = None
        self.author = None
        self.nextIds = []
        self.img_base64 = []

    def getImageCommend(self, cookie, log=False, islogin=True, isProxy=True):
        self.commend = self.relativeRecommend.format(self.illustId)
        if islogin:
            self.headers['Cookie'] = cookie
        res = req(url=self.commend, headers=self.headers, params=self.recommendParams).json()
        # print(res)
        # print(isProxy)
        if isProxy:
            pic_url, nextids = self.getCommendInfo(res, self.imgUrlProxy)
            return res, pic_url, [i for i in nextids]
        else:
            pic_url, nextids = self.getCommendInfo(res)
            self.threadDownload(self.headers, pic_url)
        # for i in self.pic_url:
        #     if i == "":
        #         continue
        #     else:
        #         byteInfo = req(i, headers=self.headers)
        #         # if log:
        #         #     logged = Logger("illust.log")
        #         #     logged.log("请求链接: %s " % self.url)
        #
        #         # 将下载的图片二进制(byteInfo.content) 解码(decode) 然后编码转为base64格式
        #         base_data = base64.encodebytes(byteInfo.content).decode("utf-8")
        #         data64.append(base_data)
        # print(len(self.img_base64))
        # img_base64_list = []
        # img_base64_list = self.img_base64[:]
        # self.img_base64.clear()
        # print(len(img_base64_list))
        # print(self.img_base64, img_base64_list)
        return res, self.img_base64
        # return res

    @staticmethod
    def getCommendInfo(res_json, imgUrlProxy=None):

        pic_url_list = []
        body = res_json["body"]['illusts']
        nextids = res_json['body']['nextIds']
        # print(nextids)
        if imgUrlProxy != None:
            for i in body:
                # print("Count: ", i.get("url"))
                if i.get("url") == None:
                    continue
                pic_url_list.append(imgUrlProxy + i.get("url")[len(imgUrlProxy):])
            return pic_url_list, nextids
        else:
            for i in body:
                # print("Count: ", i.get("url"))
                if i.get("url") == None:
                    continue
                pic_url_list.append(i.get("url"))
            return pic_url_list, nextids

    def download(self, headers, img_url, semaphore):

        semaphore.acquire()
        byte_info = req(url=img_url, headers=headers).content
        base_data = base64.encodebytes(byte_info).decode("utf-8")
        self.img_base64.append('data:image/{};base64,%s'.format(img_url.split(".")[-1]) % base_data)
        logger = Logger("request.log")
        logger.log("启动线程下载-当前: %s" % img_url)
        semaphore.release()

    def threadDownload(self, headers, urllist: List):

        # 启动多线程，允许每次执行的最大数量
        # 将图片加入线程队列
        semaphore = threading.BoundedSemaphore(default_setting.MAX_THREADING_NUM)
        threads = []
        for m in urllist:
            if m != None:
                target = Thread(target=self.download, args=[headers, m, semaphore])
                target.start()
                threads.append(target)
            else:
                continue
        # print(threads)
        for i in threads:
            i.join()

    def loadMoreCommend(self, page_num: int, page_size: int, nextIds: list):
        payload = {
            "illust_ids[]": []
        }

        if page_num == 1:
            payload['illust_ids[]'].append(nextIds[:page_size])
        else:
            payload['illust_ids[]'].append(nextIds[page_size * (page_num - 1): page_size * page_num])
        response = req(url=self.recommendMore, params=payload).json()
        return response



class PixivUser(PixivDefault):

    """
        获取pixiv用户信息
        不需要传入cookie
    """


    def __init__(self, userId):

        self.userId = userId
        super().__init__()

    @property
    def _session(self):
        return new_session()

    def getUserInfo(self):

        user_url = self.userInfoUrl.format(self.userId)
        user_top_url = self.userIllustsInfo.format(self.userId)
        session = self._session
        # session.headers['Cookie'] = cookie
        userInfo = self.userinfo_proxy_url(req(url=user_url, session=session).json(), self.imgUrlProxy)

        userIllusts = self.getUserIllusts(user_top_url, session)
        userIllusts_proxy = self.illusts_proxy_url(userIllusts, self.imgUrlProxy)

        return {"result": 200, "userInfo": userInfo, "userIllusts": userIllusts_proxy}
        # return {"result": 200}


    def getUserIllusts_Ex(self, cookie:str):

        user_top_url = self.userIllustsInfo.format(self.userId)
        session = self._session
        session.headers['Cookie'] = cookie
        userIllusts = req(url=user_top_url, session=session).json()
        return userIllusts


    @staticmethod
    def getUserIllusts(url, session):
        response = req(url=url, session=session).json()
        return response


    @staticmethod
    def userinfo_proxy_url(res: dict, proxy_url):
        user = res['body']
        # print(illusts)
        user['imageBig'] = proxy_url + user['imageBig'][len(proxy_url):]
        user['image'] = proxy_url + user["image"][len(proxy_url):]
        return res



    @staticmethod
    def illusts_proxy_url(res: dict, proxy_url):
        illusts = res['body']['illusts']
        for i in illusts:

            illusts[i]['url'] = proxy_url + illusts[i]['url'][len(proxy_url):]
            # print(illusts[i]['url'])
            # i['profileImageUrl'] = proxy_url + i['profileImageUrl'][len(proxy_url):]
        return illusts