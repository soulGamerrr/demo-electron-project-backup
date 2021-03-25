import json
import time
import logging
from logging import handlers
import requests
import random
import re
from urllib import request
# from bs4 import BeautifulSoup
import ssl

import os

ssl._create_default_https_context = ssl._create_unverified_context



USER_AGENT_POOL = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {
    # "Host": "www.pixiv.net",
# 'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
    "User-Agent": random.choice(USER_AGENT_POOL),
    # "Referer": "https://www.pixiv.net/artworks/87460236",
    # "Cookie": "_gat_UA-76252338-4=1; _ga=GA1.3.108332061.1616408105; _ga=GA1.2.108332061.1616408105; PHPSESSID=fk9vskej7pv689fg4oelanjiivijorb7; _gid=GA1.3.1175523965.1616408105; p_ab_id_2=4; _gat=1; p_ab_d_id=1087627125; __cf_bm=83c8f12c9488790fe6570c2decd138c4c68066dd-1616408105-1800-AUlv5TSIJ2dPLDmGSZa0xoIGdLl3A+Rv4zO2hL8ZR+iPjI+CQnt7GSjbARzkLNFjOOcgGETW9pWpoJjnS09kS2urQ1QEfS4+JSgpzuMdgm+FQpFgkOjb3401CqO37KCMEQ7UFg1svRLofEKksy4dXOLR8TOvZZX1Q2/7DDh+ckkooPo0dCrOZqimS6TD8gerjY1TwFDr+0+4YSJFcg+z0Ec=; __cfduid=dc851f2da248f4ddd2162b9b2f535fbb41616408104; p_ab_id=4; _gid=GA1.2.1175523965.1616408105; "
}

imgId = "87254574"

url = "https://www.pixiv.net/touch/ajax/illust/details?illust_id=" + imgId
url2 = "https://www.pixiv.net/touch/ajax/illust/details?illust_id={}".format(imgId)


params = {
    "limit":18,
    "lang":"zh"
}
# limit=18&lang=zh
# 检验
login = 'https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=pc&view_type=page'
post_key_url = "https://accounts.pixiv.net/login?"

session = requests.Session()
session.headers = headers
print("请求头", session.headers)
login_page = session.get(url=post_key_url)
# print(login_page)
post_key = re.search(r'"post_key" value="(.+?)"', login_page.text)
# print(post_key)
login_data = {
    "pixiv_id": "1264104754@qq.com",
    "password": "wyb2606078",
    "return_to": "https://www.pixiv.net",
    'ref': 'wwwtop_accounts_indes',
    # 'captcha': '',
    # 'g_reaptcha_response': '',
    "post_key": ""
}
#
login_data['post_key'] = post_key.group(1)
# # print(data)
# # #
time.sleep(3)
result = session.post(url=login, data=login_data)
print(session.cookies.get_dict(), post_key.group(1))
print(result.headers)
# 检查是否登录成功
cookie_str = ""
for key, value in session.cookies.get_dict().items():
    item_str = key + "=" + value + "; "
    cookie_str += item_str
session.headers['Cookie'] = cookie_str
print(session.headers)
time.sleep(2)
_login_check_url = 'https://www.pixiv.net/touch/ajax/user/self/status'
status = session.get(url=_login_check_url).json()
print(status)




# res_cookie = requests.get(url="https://www.pixiv.net/ajax/illust/87460236", headers=headers)
# print(res_cookie.request._cookies)
# headers['Cookie'] = res_cookie.headers.get("Set-Cookie")


# res = requests.get(url="https://www.pixiv.net/ajax/illust/87460236/recommend/init?", params=params, headers=headers,
#                    timeout=10)
# print(res)
# imginfo = res["body"]


# print(imginfo)

# {'tags': {'authorId': '16731', 'isLocked': False, 'tags': [{'tag': 'オリジナル', 'locked': True, 'deletable': False, 'userId': '16731', 'userName': '玉之けだま'}, {'tag': 'すじ', 'locked': False, 'deletable': False}, {'tag': '尻神様', 'locked': False, 'deletable': False}, {'tag': '吸血鬼', 'locked': False, 'deletable': False}, {'tag': 'おっぱい', 'locked': False, 'deletable': False}, {'tag': '貧乳', 'locked': False, 'deletable': False}, {'tag': 'オリジナル10000users入り', 'locked': False, 'deletable': False}], 'writable': False},

class Logger(object):

    level_relations = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, dirname="./log",  level="info", backUpCount=3,
                 fmt="%(asctime)s - %(pathname)s[%(funcName)s] - %("
                                                                  "levelname)s:- %(message)s"):


        if level.islower():
            level = level.upper()
        if os.path.exists(dirname):
            print("文件夹存在")
        else:
            try:
                os.makedirs(dirname)
                print("创建成功")
            except Exception as e:
                print("创建失败", e)

        # 注册文件的文件名
        savePath = dirname + filename
        self.logger = logging.getLogger()
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.RotatingFileHandler(filename=savePath, mode="a", backupCount=backUpCount, maxBytes=1048576,
                                          encoding='utf-8')
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

#
# filename = "/debug.json"
# log = Logger(filename, level="debug")
# log.logger.info(imginfo)


# ids = ['86363351', '82470956', '87033381', '84002881', '82255338', '85954430', '86109040', '86825740', '86108522',
#   '87159236', '83635800', '86704683', '84169885', '87349168', '87266682', '86610555', '86936570', '71936516', '87462909', '86753467', '83252877', '84172315', '87543224', '84670855', '84987041', '87440690', '86918126', '81095797', '86929329', '76081770', '83996011', '87013557', '86162732', '85384714', '87146762', '58938270', '86650720', '87090111', '86860422', '86503174', '87277901', '69029152', '86972597', '87261433', '86885193', '84617879', '86316256', '87432149', '86464572', '73260941', '87091410', '84189840', '87013646', '87119635', '86941614', '87128515', '87040996', '85339949', '85583616', '87279353', '84958655', '87360339', '86885312', '87415978', '81411186', '86872640', '84932457', '84907947', '84590299', '86240244', '84480547', '85228373', '87507995', '85580604', '81879815', '80132896', '86452425', '87469781', '86368251', '87254711', '83672006', '86016044', '84503628', '84503703', '86238865', '85281471', '86917612', '83955499', '86914161', '87420063', '84442505', '83997579', '86539228', '81585971', '85808574', '85627286', '86015873', '86266633', '87326565', '79957867', '86055824', '87155082', '87097839', '85672405', '82989914', '85139499', '84399407', '82701799', '82276630', '86483658', '72552061', '85147663', '86537618', '78788966', '86460380', '84673133', '81471822', '84136640', '81672780', '81692909', '84503667', '82284542', '86919436', '86101782', '87232493', '85767635', '81411237', '84409977', '85217066', '86037371', '81910735', '87523165', '82685776', '82234981', '84758203', '86300984', '81649643', '79834844', '85918824', '86300329', '83866531', '86931879', '83804670', '82903619', '79835955', '85672423', '85496945', '85101173', '80808808', '87453106', '86253142', '84660354', '85673772', '87230329', '85612660', '87415895', '87229500', '86555522', '87406211', '81519031']
#
# idss = "https://www.pixiv.net/ajax/illust/recommend/illusts?illust_ids%5B%5D=79117133&illust_ids%5B%5D=59503412&illust_ids%5B%5D=79598885&illust_ids%5B%5D=85208097&illust_ids%5B%5D=85219851&illust_ids%5B%5D=83989168&illust_ids%5B%5D=70624275&illust_ids%5B%5D=70966108&illust_ids%5B%5D=78492610&illust_ids%5B%5D=61082722&illust_ids%5B%5D=84697223&illust_ids%5B%5D=80594549&illust_ids%5B%5D=81135285&illust_ids%5B%5D=86560114&illust_ids%5B%5D=78346150&illust_ids%5B%5D=86464563&illust_ids%5B%5D=82673558&illust_ids%5B%5D=55559245&lang=zh"
# res = requests.get(url=idss, headers=headers)
# print(res.json())
