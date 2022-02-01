import os
import requests

# 学号
loginId = os.environ["LOGIN_ID"]
# 密码
loginPwd = os.environ["LOGIN_PWD"]
# 户籍
householdRegister = os.environ["HOUSEHOLD_REGISTER"]
# 手机号码
phoneNumber = os.environ["PHONE_NUMBER"]
# 当前位置
currentLocation = os.environ["CURRENT_LOCATION"]
# 是否在校:0不在,1在
isSchool = 0

class TB:
    def __init__(self, id, pwd, home, phone, city='浙江省温州市瓯海区', school=1):
        self.__httpClient = requests.Session()
        self.loginId = id
        self.loginPwd = pwd
        self.home = home
        self.phone = phone
        self.city = city
        self.school = school

    def login(self):
        url = 'https://info2.webvpn.wzvtc.cn/supply/check_wx.jsp'
        data = {'name': self.loginId, 'abc': self.loginPwd}
        loginResp = self.__httpClient.post(url=url, data=data)
        return loginResp.status_code == 200 and loginResp.text.find(self.loginId)

    def getMyBan(self):
        url = 'https://info2.webvpn.wzvtc.cn/supply/disp_myban.jsp'
        mybanResp = self.__httpClient.get(url)

    def put(self):
        # url = 'https://info2.webvpn.wzvtc.cn/supply/put.jsp'
        url = 'https://info2.webvpn.wzvtc.cn/supply/wx/put.jsp'
        charset = 'GBK'
        req = {'b1': bytes(self.home, charset),
               'b3': bytes(self.city, charset),
               'b2': self.phone,
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
               'ab': self.school,
               'ac': 0,
               'ac1': '',
               'ac2': ''}
        resp = self.__httpClient.post(url=url, data=req)
        return resp.status_code == 200 and (resp.text.find('填报成功！') or resp.text.find('已经申报成功，请勿重复提交！'))


tb = TB(loginId, loginPwd, householdRegister,
        phoneNumber, currentLocation, isSchool)
if (tb.login() and tb.put()):
    print("填报成功")
else:
    print("填报失败")
