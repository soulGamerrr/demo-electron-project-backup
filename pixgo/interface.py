import base64
import json
import pickle
import sys
import threading
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
    recommendParams = {
        "limit": 20,
        "lang": "zh"
    }
    headers = settings.DEFAULT_HEADER_HANDLER

    # 仅限图片代理，并不会访问pixiv
    imgUrlProxy = "https://i.pixiv.cat"


#     https://i.pixiv.cat/c/540x540_70/img-master/img/2021/01/24/02/53/01/87254574_p0_master1200.jpg'

class PixivHome(PixivDefault):

    def __init__(self):
        super().__init__()

    @property
    def _session(self):
        return new_session()

    # 首页请求接口，返回为字典类型
    def homePage(self, cookie: str, type: str = settings.DEFAULT_TYPE, mode: str = settings.DEFAULT_MODE) -> dict:

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
        response = req(url=self.illustHome.format(use_type, use_mode), session=session).json()
        body = response['body']
        rank_list = self.home_rank_info(body)
        rank_list_url_info = self.loadMore_ids(rank_list)
        print(rank_list_url_info)
        return {"result": 200, "items": rank_list_url_info}

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
        print(rank_ids_lsit)
        return rank_ids_lsit

    @staticmethod
    def loadMore_ids(rank_list: list):
        payload = {
            "illust_ids[]": []
        }
        url = "https://www.pixiv.net/ajax/illust/recommend/illusts?"
        payload['illust_ids[]'].append(rank_list)
        response = req(url=url, params=payload).json()
        return response

    @staticmethod
    def get_illust_url(load_more):
        



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
        semaphore = threading.BoundedSemaphore(settings.MAX_THREADING_NUM)
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
