import os
import random
import requests
from typing import Tuple

##########

login_account = os.environ["LOGIN_ACCOUNT"]                 # 学号
login_password = os.environ["LOGIN_PASSWORD"]               # 密码
household_register = os.environ["HOUSEHOLD_REGISTER"]       # 户籍所在地
phone_number = os.environ["PHONE_NUMBER"]                   # 联系电话
current_location = os.environ["CURRENT_LOCATION"]           # 当前所在地
serverChan_key = os.environ["SERVERCHAN_KEY"]               # Server 酱 Key
at_school = 0                                               # 0：不在  1：在
send_message = True                                         # 1：发送(默认)  0：不发送

try:
    serverChan_key = os.environ["SERVERCHAN_KEY"]           # Server 酱 Key
except:
    send_message = False                                    # 若未配置 Key ，则不发送信息

##########

# 健康填报模块

class HealthReport:
    def __init__(self, login_account, login_password, household_register, phone_number, current_location, at_school):
        self.__httpClient = requests.Session()
        self.login_account = login_account
        self.login_password = login_password
        self.household_register = household_register
        self.phone_number = phone_number
        self.current_location = current_location
        self.at_school = at_school

    def login(self) -> Tuple[int, str]:
        URL = "https://info2.webvpn.wzvtc.cn/supply/check_wx.jsp"
        data = {'name': self.login_account, 'abc': self.login_password}
        loginResponse = self.__httpClient.post(url=URL, data=data)
        return loginResponse.status_code, loginResponse.text

    def report(self) -> Tuple[int, str]:
        # URL = "https://info2.webvpn.wzvtc.cn/supply/put.jsp"
        URL = "https://info2.webvpn.wzvtc.cn/supply/wx/put.jsp"
        charset = 'GBK'
        reportData = {
            'b1': bytes(self.household_register, charset),  # 户籍所在地
            'b3': bytes(self.current_location, charset),    # 现所在地
            'b2': self.phone_number,                        # 手机号码
            'a1': 0,
            'a11': bytes('请点击并填写实测体温', charset),
            'a2': 0,
            'a21': bytes('请点击并填写实测体温', charset),
            'a3': 0,
            'a4': 0,
            'a41': bytes('如有，请点击并填写说明', charset),
            'a5': 0,
            'a51': '',
            'a52': '',
            'a6': 0,
            'a61': '',
            'a62': '',
            'a63': 0,
            'a631': '',
            'a7': 0,
            'a71': '',
            'a72': '',
            'a73': '',
            'a8': 1,
            'a81': '',
            'a9': 0,
            'a91': '',
            'a92': '',
            'a93': '',
            'a94': 0,
            'aa': 0
        }
        # 于 2022/8/30 提交中未发现如下参数
        # 'ab': self.at_school,
        # 'ac': 0,
        # 'ac1': '',
        # 'ac2': ''
        # }
        reportResponse = self.__httpClient.post(url=URL, data=reportData)
        return reportResponse.status_code, reportResponse.text

# 信息发送模块

class MessageSend:
    def __init__(self, serverChan_key):
        self.__httpClient = requests.Session()
        self.serverChan_key = serverChan_key
        self.send_message = send_message

    def send(self, title, message):
        if self.send_message:
            url = f"https://sctapi.ftqq.com/{serverChan_key}.send"
            data = {'title': title, 'desp': message}
            messageSendResponse = requests.post(url=url, data=data)
            return messageSendResponse.status_code


def warp(string: list) -> str:
    return "\n".join(string)


def daily_random_number():
    return str(random.randint(10, 30))


health_reporter = HealthReport(login_account=login_account, login_password=login_password,
                               household_register=household_register, phone_number=phone_number,
                               current_location=current_location, at_school=at_school)

message = MessageSend(serverChan_key=serverChan_key)

login_status, login_return_text = health_reporter.login()

if login_status == 200 and login_return_text.__contains__(login_account):
    if login_return_text.__contains__("你今天已经做过申报，如果因填错需要重新填报的，请联系辅导员先删除今天的填报记录！"):
        message.send("已于今日早些时间完成填报！")

    elif login_return_text.__contains__("当前时间不在填报时间范围内！"):
        message.send("如果现在还没填报的话那你大概是无了……")

    else:
        report_status, report_return_text = health_reporter.report()

        if report_status == 200 and report_return_text.__contains__("填报成功！"):
            message.send(f"成功完成填报，已为您节省 {daily_random_number()} 秒！")

        elif report_status == 200 and report_return_text.__contains__("已经申报成功，请勿重复提交！"):
            message.send("已经申报成功，请勿重复提交！")

        else:
            print(warp([
                f"{report_status}",
                f"{report_return_text}"
            ]))
            message.send(
                f"出现错误, HTTP 状态码: {report_status}", report_return_text)

else:
    print(warp([
        login_account,
        login_return_text
    ]))
    message.send(f"出现错误, HTTP 状态码: {login_status}", login_return_text)
