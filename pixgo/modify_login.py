import json
import os
import random
import time
import hashlib
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=pc&view_type=page"

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
    "Host": "www.pixiv.net",
        "User-Agent": random.choice(USER_AGENT_POOL),
        # "Referer": "https://www.pixiv.net/artworks/87460236",
        # "Cookie": "ki_t=1613366493740%3B1613366493740%3B1613366497403%3B1%3B2;__utmb=235335808.2.10.1613366492;_ga=GA1.2.364945617.1613366482;ki_r=;__utmv=235335808.|3=plan=normal=1^6=user_id=43685708=1^11=lang=zh=1;__utmc=235335808;c_type=23;b_type=0;a_type=0;device_token=5ebbaf6617eff7ea89a705027230eb0f;PHPSESSID=43685708_wpii1v2sf8weoXdadnlQ2G9H2DgY8qbr;__utma=235335808.364945617.1613366482.1613366492.1613366492.1;privacy_policy_agreement=0;first_visit_datetime_pc=2021-02-15+14%3A21%3A31;p_ab_id_2=8;__utmt=1;yuid_b=OWUpI0A;__utmz=235335808.1613366492.1.1.utmcsr=accounts.pixiv.net|utmccn=(referral)|utmcmd=referral|utmcct=/login;__cfduid=dec0caa83ef232ea5a7582da394dfb7b21613366479;p_ab_id=4;__cf_bm=5cd2e3e94b5e8eb2074d9d14ed56b339cfb7caaf-1613366481-1800-Af2auWJLacoRWKMC8lrcaaPJf7vkbjJELVvba1xmfxowgiiw6AveEFiNHJ2tbwSuHVrQnTZkSfmiIOs0/xVzhPm9WrMuEyUM3G38CwM4XKzi0Ucy654bSfvzEruh9W+e7Ba7SToIdZ07OdMB3Je8wwJ+LZUwLgIoi9La3RK5b1lTo0dlZpqcQiKp2QqX9YTCCtPZBmOHHN16glpleonTkjU=;_gat=1;p_ab_d_id=1321842689;_gid=GA1.2.1444110736.1613366482;"
}



def _login(user_id, pword):

    hex_digital_user_name = hashlib.md5(user_id.encode("utf-8")).hexdigest()
    # print(type(hex_digital_user_name))
    # flag = LoginChecked(hex_digital_user_name)
    # print(flag)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome("C:\\chromedriver\\chromedriver.exe", options=options)
    print("尝试进行登录....")
    driver.implicitly_wait(5) # seconds
    driver.get(url=url)
    # time.sleep(5)
    username = driver.find_element_by_xpath("//*[@id='LoginComponent']/form/div[1]/div[1]/input")
    password = driver.find_element_by_xpath("//*[@id='LoginComponent']/form/div[1]/div[2]/input")
    username.send_keys(
        user_id)
    password.send_keys(pword)
    print(username, password)
    print("登录完成....")
    driver.find_element_by_xpath("//*[@id='LoginComponent']/form/button").click()
    time.sleep(5)
# print(username, password)
#     driver.refresh()
    c = driver.get_cookies()
    item_str = ""
    cookie_str = ""
    for item in c:
        item_str = item["name"] + "=" + item["value"] + "; "
        cookie_str += item_str
    # print(cookie_str)
    time.sleep(2)
    result = loginCheck(cookie_str)
    print(result)
    if result['result'] == 200:
        return result
    else:
        return result
    # file_name = hex_digital_user_name + ".data"
    # save_user_cookie(cookie_str.encode("utf-8"), file_name)

# def LoginChecked(hexdigit):
#
#     message = load_user_cookie(hexdigit)
#     print(2, "-", message)
#     if message['file']:
#         print(3, "-登录检测")
#         session = requests.Session()
#         headers['Cookie'] = message['cookie'].decode("utf-8")
#         session.headers = headers
#         _login_check_url = 'https://www.pixiv.net/touch/ajax/user/self/status'
#         resp = session.get(url=_login_check_url).json()
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

def loginCheck(cookie):

    session = requests.Session()
    session.headers = headers
    session.headers["Cookie"] = cookie
    _login_check_url = 'https://www.pixiv.net/touch/ajax/user/self/status'
    resp = session.get(url=_login_check_url).json()

    if resp['body']['user_status']["is_logged_in"] == True:
        print(4, "-用户已登录！")
        userInfo = resp['body']["user_status"]
        # 头像获取
        profile_img = userInfo['profile_img']['main']
        return {"result": 200, "status": True, "error": False, "profile_img": profile_img}
    else:
        print(4, "-用户未登录")
        # print(resp)
        return {"result": 100, "status": False, "error": True, "info": resp}



# def save_user_cookie(cookie, file_name):
#     if not os.path.exists(file_name):
#         with open(file_name, "wb") as f:
#             f.write(cookie)
#     else:
#         with open(file_name, "wb") as f:
#             f.write(cookie)
#
# def load_user_cookie(hexdigit):
#
#     # 将用户登录的用户名作为文件名进行存储
#     file_name = hexdigit + ".data"
#     try:
#         if os.path.exists(file_name):
#             with open(file_name, "rb") as f:
#                 cookie = f.readline()
#             if not len(cookie) == 0:
#                 print(1, "-文件存在，读取信息！")
#                 return {"file": True, "msg": "File read successfully!", "cookie": cookie}
#         else:
#             raise FileNotFoundError
#     except FileNotFoundError as e:
#         print(1, "-文件未找到，重新创建")
#         return {"file": False, "msg": "File not found, need login!"}

_login("1264104754@qq.com", "wyb2606078")
