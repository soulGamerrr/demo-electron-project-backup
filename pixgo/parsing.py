"""
    此模块针对url响应的一些信息进行解析并组装
"""
import os
import re
import time
import logging
import requests

from . import settings
from . import httpError

from logging import handlers



class Logger(object):
    level_relations = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, dirname=None, level="info", backUpCount=3,
                 fmt="%(asctime)s - %(pathname)s[%(module)s - %(funcName)s %(lineno)s] - %("
                     "levelname)s:- %(message)s"):

        # 若输出的日志等级不为全大写，或是全小写，则转化为大写
        if level.islower():
            level = level.upper()

        if dirname == None:
            dirname = settings.LOG_SAVE_FILE_PATH

        if os.path.exists(dirname):
            pass
        else:
            try:
                os.makedirs(dirname)
                print("创建成功")
            except Exception as e:
                print("创建失败", e)

        savePath = dirname + filename
        # 注册文件的文件名
        self.logger = logging.getLogger(filename)
        self.format_str = logging.Formatter(fmt)
        # 如果有已经注册的日志logger, 判断是否注册，否则，打印日志会出现以下情况，第一次打印一条，第二次打印两条，以此类推。
        # 不符合日志写入规则和条件
        if not self.logger.handlers:
          # 设置日志格式
            self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
            self.sh = logging.StreamHandler()  # 往屏幕上输出
            self.sh.setFormatter(self.format_str)  # 设置屏幕上显示的格式
            self.th = handlers.RotatingFileHandler(filename=savePath, mode="a", backupCount=backUpCount, maxBytes=1048576,
                                                   encoding='utf-8')

            self.th.setFormatter(self.format_str)  # 设置文件里写入的格式
            self.logger.addHandler(self.sh)  # 把对象加到logger里
            self.logger.addHandler(self.th)

    # 传入文本内容为自定义写日志内容
    def log(self, text, level=settings.LOG_INFO):

        if not level.isupper():
            level = level.upper()
        try:
            if isinstance(text, str):
                if level == "DEBUG":
                    self.logger.debug(text)
                    # self.logger.removeHandler(self.sh)
                    # self.logger.removeHandler(self.th)
                    return
                elif level == "INFO":
                    self.logger.info(text)
                    # self.logger.removeHandler(self.sh)
                    # self.logger.removeHandler(self.th)
                    return
                elif level == "WARNING":
                    self.logger.warning(text)
                    # self.logger.removeHandler(self.sh)
                    # self.logger.removeHandler(self.th)
                    return
                elif level == "ERROR":
                    self.logger.error(text)
                    # self.logger.removeHandler(self.sh)
                    # self.logger.removeHandler(self.th)
                    return
        except TypeError as e:
            self.logger.error(e)


# 封装requests
def req(url, req_type="get", session=None, headers=settings.DEFAULT_HEADER_HANDLER,
        timeout=settings.TIMEOUT, reties=settings.MAX_RETRIES_REQUESTS, requester=None, data=None, params=None):
    logged = Logger("request.log")
    curr_reties = 1
    req_type = req_type.upper()
    if requester == None:
        handler = requests if session == None else session
        requester = handler.get if req_type == "GET" else handler.post
    while curr_reties <= reties:

        try:
            res = requester(url=url, headers=headers, timeout=timeout, data=data, params=params)
            # print(res.headers)
            # if res.status_code == 200:
            #     logged.log("请求链接: %s " % url + params)
            #     logged.log("请求状态码: %d " % res.status_code + "成功!")
            #     return res
            # else:
            #     logged.log("请求链接: %s " % url + params)
            #     logged.log("请求状态码: %d " % res.status_code + "失败!")
            if res.status_code == 200:
                checked = httpError.HTTP_REQUEST_SUCC.get(str(res.status_code))
                logged.log("请求链接: %s " % url)
                logged.log(checked.format(req_type))
                return res
            else:
                checked = httpError.HTTP_REQUEST_ERROR.get(str(res.status_code))
                logged.log("请求链接: %s " % url)
                logged.log(checked)
                return res

        except requests.exceptions.Timeout as e:
            logged.log("重试次数：%s " % curr_reties + "请求连接超时.... "
                                                  "Wait for {} seconds and try again".format(settings.REQUESTS_DELAY))
            print("重试次数：%s" % curr_reties, "请求连接超时", e)
        except requests.exceptions.ConnectionError as e:
            logged.log("重试次数：%s " % curr_reties + "连接错误.... "
                                                  "Wait for {} seconds and try again".format(settings.REQUESTS_DELAY))
            # print("重试次数：%s" % curr_reties, "连接错误", e)
        except requests.exceptions.RequestException as e:
            logged.log("重试次数：%s " % curr_reties + "请求错误.... "
                                                  "Wait for {} seconds and try again".format(settings.REQUESTS_DELAY))
            print("重试次数：%s" % curr_reties, "请求错误", e)

        curr_reties += 1
        # 等待一秒后重新尝试
        time.sleep(settings.REQUESTS_DELAY)

    raise requests.exceptions.RetryError


# 对response 响应信息进行处理， 如果为json数据直接转换
def _load_json_res(res):
    pass


# 使用re模块取页面必要信息
def ruleFindImgDetail(text):
    imgInfo = dict()

    _rule_find_name = re.compile(pattern=r'"user_name":"(.+?)"')
    # _rule_find_mid = re.compile(pattern=r'"illustId":"(\d+)"')
    _rule_find_mid = re.compile(pattern=r'illust_id=(\d+)"')
    # _rule_find_original_url = re.compile(pattern=r"https://i.pximg.net/img-original.+?\.png")
    _rule_find_original_url = re.compile(pattern=r'"url_big":"(.+?)"')
    # _rule_find_img_info = re.compile()

    imgInfo['illustId'] = _rule_find_mid.findall(text)[0]
    imgInfo['userName'] = _rule_find_name.findall(text)[0].encode("utf-8").decode("unicode_escape")
    imgInfo['originalUrl'] = "".join(_rule_find_original_url.findall(text)[0].split("\\"))

    # illustId = _rule_find_mid.findall(text)[0]
    # userName = _rule_find_name.findall(text)[0].encode("utf-8").decode("unicode_escape")
    # # original_url = _rule_find_original_url.findall(text)[0]
    # originalUrl = "".join(_rule_find_original_url.findall(text)[0].split("\\"))
    # print(mid, userName, original_url)

    return imgInfo


def getJson(text):
    imgInfo = dict()
    # All of this pic's image url type, 当前图片所有大小的链接
    body = text.json()['body']
    imgInfo['illustId'] = body['illustId']
    imgInfo['userName'] = body["userName"]
    imgInfo = body['urls']
    imgInfo['tags'] = body['tags']['tags']
    print(imgInfo)
    return imgInfo


# 写文件
def write(url, headers, timeout, savePath=None, fileName=None):
    fileName = url.split("/")[-1]
    print("写入文件路径 %s" % savePath)
    if not savePath:
        savePath = settings.DEFAULT_ILLUST_SAVE_PATH
    if os.path.exists(savePath):
        print("文件夹存在")
    else:
        try:
            os.makedirs(savePath)
            print("创建成功")
        except Exception as e:
            print("创建失败", e)
    reties = 1
    while reties <= 3:
        try:
            url_download = req(url, headers=headers, timeout=timeout).content
            with open(savePath + fileName, "wb") as f:
                f.write(url_download)
            return "illust download finished!!"
        except:
            raise TimeoutError
        reties += 1
        time.sleep(.5)
        print("重试第 %s 次" % reties)


def new_session():

    return requests.Session()
