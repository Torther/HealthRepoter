import os
import requests
from typing import Tuple

##########

login_account = os.environ["LOGIN_ACCOUNT"]
login_password = os.environ["LOGIN_PASSWORD"]
household_register = os.environ["HOUSEHOLD_REGISTER"]
phone_number = os.environ["PHONE_NUMBER"]
current_location = os.environ["CURRENT_LOCATION"]
serverChan_key = os.environ["SERVERCHAN_KEY"]
at_school = 0  # 0：不在  1：在
send_message = 1  # 1：发送  0：不发送


##########


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
        reportData = {  # 外包的我囸你先人
            'b1': bytes(self.household_register, charset),
            'b3': bytes(self.current_location, charset),
            'b2': self.phone_number,
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
            'aa': 0,
            'ab': self.at_school,
            'ac': 0,
            'ac1': '',
            'ac2': ''
        }
        reportResponse = self.__httpClient.post(url=URL, data=reportData)
        return reportResponse.status_code, reportResponse.text


class MessageSend:
    def __init__(self, serverChan_key):
        self.__httpClient = requests.Session()
        self.serverChan_key = serverChan_key
        self.send_message = int2bool(send_message)

    def send(self, title, message):
        if self.send_message:
            url = f"https://sctapi.ftqq.com/{serverChan_key}.send"
            data = {'title': title, 'desp': message}
            messageSendResponse = requests.post(url=url, data=data)
            return messageSendResponse.status_code


def warp(string: list) -> str:
    return "\n".join(string)


def int2bool(v: int) -> bool:
    if isinstance(v, bool):
        return v
    elif v == 1:
        return True
    elif v == 0:
        return False


health_reporter = HealthReport(login_account=login_account, login_password=login_password,
                               household_register=household_register, phone_number=phone_number,
                               current_location=current_location, at_school=at_school)

message = MessageSend(serverChan_key=serverChan_key)

login_status, login_return_text = health_reporter.login()

if login_status == 200 and login_return_text.__contains__(login_account):
    if login_return_text.__contains__("你今天已经做过申报，如果因填错需要重新填报的，请联系辅导员先删除今天的填报记录！"):
        print("已填报过！")
        message.send("已填报过！", "已填报过！")
    elif login_return_text.__contains__("当前时间不在填报时间范围内！"):
        print("当前时间不在填报时间范围内！")
        message.send("当前时间不在填报时间范围内！", "当前时间不在填报时间范围内！")
    else:
        report_status, report_return_text = health_reporter.report()
        if report_status == 200 and report_return_text.__contains__("填报成功！"):
            print("填报成功！")
            message.send("填报成功！", "填报成功！")
        elif report_status == 200 and report_return_text.__contains__("已经申报成功，请勿重复提交！"):
            print("已经申报成功，请勿重复提交！")
            message.send("已经申报成功，请勿重复提交！", "已经申报成功，请勿重复提交！")
        else:
            print(warp([
                f"{report_status}",
                f"{report_return_text}"
            ]))
            message.send(f"出现错误,状态码：{report_status}", report_return_text)
else:
    print(warp([
        login_account,
        login_return_text
    ]))
    message.send(f"出现错误,状态码：{login_status}", login_return_text)
