import re
import os
import time
import json
import requests
import random

from pixgo import default_setting
# from .parsing import _rule_find_img_detail, write

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


filePath = default_setting.ILLUST_FOLDER_SAVE
timeout = default_setting.TIMEOUT
#
#
# def downloadOne(url, imgId, headers):
#
#     try:
#         res = requests.get(url=url, headers=headers, timeout=timeout)
#         if res.status_code == 200:
#             print("访问页面成功，返回页面信息")
#             text = res.text
#             mid, userName, url = _rule_find_img_detail(text)
#             time.sleep(.5)
#             savePath = filePath.format(userName)
#             write(url, headers, timeout, savePath, fileName=url.split("/")[-1])
#             print("原图最终路径: ", url, mid, userName)
#     except Exception as e:
#         print(e)
#
# # url = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}".format(userId)
#
#
#
# if __name__ == "__main__":
#
#     imgId = input("仅支持图片ID： ")
#     while True:
#         if imgId.isdigit():
#             break
#         else:
#             imgId = input("仅支持图片ID： ")
#     url = "https://www.pixiv.net/touch/ajax/illust/details?illust_id={}".format(imgId)
#     headers = settings.DEFAULT_HEADER_HANDLER
#     headers['Referer'] = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}".format(imgId)
#
#     downloadOne(url=url, imgId=imgId, headers=headers)


