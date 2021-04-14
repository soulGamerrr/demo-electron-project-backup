"""
    这里包含了基本的配置信息，可以进行修改
"""
import random

"""
    默认请求头设置
"""
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

"""
    主页面默认参数设置
"""

DEFAULT_TYPE = "illust"
DEFAULT_MODE = "all"


DEFAULT_HEADER_HANDLER = {
    "Referer": "https://www.pixiv.net",
    "User-Agent": random.choice(USER_AGENT_POOL),
    "Host": "www.pixiv.net",
    "Accept": "*/*",
}

"""
    requests请求最大等待时间 10 s
"""

TIMEOUT = 10

"""
    最大尝试重新连接次数 3 次
"""

MAX_RETRIES_REQUESTS = 3

"""
    再次连接等待时间  3s 默认为3s
"""

REQUESTS_DELAY = 3

"""
    记录日志信息等级分为 DEBUG < INFO < WARNING < ERROR < CRITICAL
"""
LOG_SAVE_FILE_PATH = "./log/"
LOG_DEFAULT_LEVLE = "info"
LOG_INFO = "INFO"
LOG_ERROR = "ERROR"
LOG_DEBUG = "DEBUG"
LOG_WARNING = "WARNING"



"""
    ImgSave_Folder 图片保存位置初始设置
"""

ILLUST_FOLDER_SAVE = "./illusts/{0}/" # 作者name和图片mid
DEFAULT_ILLUST_SAVE_PATH = "./Default_illusts/"


"""
    获取一张图片时并获取这张图片下的相关推荐作品
"""
# 一次最多获取20张图片 可自定义
ILLUST_COMMEND_LIMIT = 18



"""
    存储cookie 的文件
"""

COOKIE_FILE = "server/cookie.data"


"""
    threading 允许每次执行的线程数量
"""

MAX_THREADING_NUM = 3




