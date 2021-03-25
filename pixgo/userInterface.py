import hashlib
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

# from pixivgo.pixgo import settings
from . import settings
from .parsing import req, new_session, Logger

class BaseClient(object):

    _login_check_url = 'https://www.pixiv.net/touch/ajax/user/self/status'
    log = Logger("request.log", level="error")

    def __init__(self):
        # self._cookie_file = settings.COOKIE_FILE
        self._headers = settings.DEFAULT_HEADER_HANDLER
        self._session = new_session()
        self._session.headers = self._headers

    # def _check_is_logged(self, hexdigit):
    #
    #     message = self._load_user_cookie(hexdigit)
    #     print(2, "-", message)
    #     if message['file']:
    #         print(3, "-登录检测")
    #         self._session.headers =  message['cookie'].decode("utf-8")
    #         # _login_check_url = 'https://www.pixiv.net/touch/ajax/user/self/status'
    #         resp = req(url=self._login_check_url, session=self._session).json()
    #         if resp['body']['user_status']["is_logged_in"] == True:
    #             print(4, "-用户已登录！")
    #             return True
    #         else:
    #             print(4, "-用户未登录")
    #             # print(resp)
    #             return False
    #     else:
    #         # need login
    #         print(4, "-false")
    #         return False

    def _check_is_logged(self, cookie):

        # message = self._load_user_cookie(hexdigit)

        print(3, "-登录检测")
        # cookie 为一串字符串需要拼接
        self._session.headers["Cookie"] = cookie
        # _login_check_url = 'https://www.pixiv.net/touch/ajax/user/self/status'
        resp = req(url=self._login_check_url, session=self._session).json()
        # print(resp)
        if resp['body']['user_status']["is_logged_in"] == True:
            print(4, "-用户已登录！")
            user_info = resp['body']["user_status"]
            # 头像获取
            profile_img = user_info['profile_img']['main']
            user_name = user_info['user_name']
            return {"result": 200, "status": True, "error": False, "profile_img": profile_img, "userName": user_name, "is_logged_in": True}
        else:
            print(4, "-用户未登录")
            # print(resp)
            return {"result": 100, "status": False, "error": True}

    #
    def _save_user_cookie(self, file_name, userCookie):

        if not os.path.exists(file_name):
            self.log.log("文件未创建，开始创建文件！\n 写入用户的COOKIE信息！")
            with open(file_name, "wb") as f:
                f.write(userCookie)
        else:
            with open(file_name, "wb") as f:
                f.write(userCookie)

    def _load_user_cookie(self, hexdigit):

        file_name = hexdigit + ".data"
        try:
            if os.path.exists(file_name):
                with open(file_name, "rb") as f:
                    cookie = f.readline()
                if not len(cookie) == 0:
                    # print(1, "-文件存在，读取信息！")
                    return {"file": True, "msg": "File read successfully!", "cookie": cookie}
            else:
                raise FileNotFoundError
        except FileNotFoundError as e:
            # print(1, "-文件未找到，重新创建")
            return {"file": False, "msg": "File not found, need login!"}
    #
    #
    # def _login(self, *args, **kwargs):
    #     raise NotImplementedError


class UserLogin(BaseClient):


    def __init__(self):

        super().__init__()
        # self.hex_digital_user_name = login_id
        # self.password = login_pwd

    def _login(self, user_id, pwd):

        # login url
        url = "https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=pc&view_type=page"
        home = "https://www.pixiv.net"
        # hex_digital_user_name = hashlib.md5(user_id.encode("utf-8")).hexdigest()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('blink-settings=imagesEnabled=false')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument("--no-sandbox") # 针对linux运行报错的情况 加上就对了
        driver = webdriver.Chrome(executable_path=r"C:\\chromedriver\\chromedriver.exe", options=options)
        # driver = webdriver.Chrome(executable_path=r"/usr/bin/chromedriver", options=options)

        print("获取链接：%s" % url)
        # driver.implicitly_wait(5)  # seconds
        driver.get(url=url)
        # time.sleep(5)
        # 填入参数
        print("开始填写参数")
        random_time = [0.3, 0.5, 0.7, 0.9, 1.1]
        username = driver.find_element_by_xpath("//*[@id='LoginComponent']/form/div[1]/div[1]/input")
        password = driver.find_element_by_xpath("//*[@id='LoginComponent']/form/div[1]/div[2]/input")
        username.send_keys(
            user_id)
        time.sleep(random.choice(random_time))
        password.send_keys(pwd)
        print("信息填写完成")
        driver.find_element_by_xpath("//*[@id='LoginComponent']/form/button").click()
        time.sleep(6)
        # print(username, password)
        driver.refresh()
        c = driver.get_cookies()
        # print(c)
        item_str = ""
        cookie_str = ""
        for item in c:
            item_str = item["name"] + "=" + item["value"] + "; "
            cookie_str += item_str
        # file_name = hex_digital_user_name + ".data"
        print(cookie_str)
        driver.quit()
        result = self._check_is_logged(cookie_str)
        if result['result'] == 200:
            print("登录成功")
            return {
                "error": False, "cookie": cookie_str, "userName": result['userName'], "is_logged_in": True, "result": 200, "profile_img":
                result['profile_img']
            }
        else:
            return {
                "error": True, "message": "出现无法判断的错误", "is_logged_in": False, "result": 100
            }


