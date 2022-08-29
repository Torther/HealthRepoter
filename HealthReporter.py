import os
import requests

loginAccount = os.environ["LOGIN_ACCOUNT"]
loginPassword = os.environ["LOGIN_PASSWORD"]
householdRegister = os.environ["HOUSEHOLD_REGISTER"]
phoneNumber = os.environ["PHONE_NUMBER"]
currentLocation = os.environ["CURRENT_LOCATION"]
serverChanKey = os.environ["SERVERCHAN_KEY"]
isSchool = 0 # 0 = 不在 1 = 在

class HealthRepoter:
    def __init__(self, loginAccount, loginPassword, householdRegister, phoneNumber, currentLocation, isSchool):
        self.__httpClient = requests.Session()
        self.loginAccount = loginAccount
        self.loginPassword = loginPassword
        self.householdRegister = householdRegister
        self.phoneNumber = phoneNumber
        self.currentLocation = currentLocation
        self.isSchool = isSchool

    def login(self):
        url = 'https://info2.webvpn.wzvtc.cn/supply/check_wx.jsp'
        data = {'name': self.loginAccount, 'abc': self.loginPassword}
        loginResponse = self.__httpClient.post(url=url,data=data)
        return loginResponse.status_code, loginResponse.text

    def report(self):
        # url = 'https://info2.webvpn.wzvtc.cn/supply/put.jsp'
        url = 'https://info2.webvpn.wzvtc.cn/supply/wx/put.jsp'
        charset = 'GBK'
        reportData = {'b1': bytes(self.householdRegister, charset),
               'b3': bytes(self.currentLocation, charset),
               'b2': self.phoneNumber,
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
               'ab': self.isSchool,
               'ac': 0,
               'ac1': '',
               'ac2': ''}
        reportResponse = self.__httpClient.post(url=url, data=reportData)
        return reportResponse.status_code, reportResponse.text

class MessageSend:
    def __init__(self,serverChanKey):
        self.__httpClient = requests.Session()
        self.serverChanKey = serverChanKey
    
    def send(title, message):
        url = 'https://sctapi.ftqq.com/'+serverChanKey+".send"
        data = {'title': title, 'desp': message}
        messageSendResponse = requests.post(url=url, data=data)
        return messageSendResponse.status_code
        

executeHealthRepoter = HealthRepoter(loginAccount, loginPassword, householdRegister, phoneNumber, currentLocation, isSchool)

loginStatusCode, loginReturnText = executeHealthRepoter.login()

if(loginStatusCode == 200 and loginReturnText.find(loginAccount)>0):
    if(loginReturnText.find("你今天已经做过申报，如果因填错需要重新填报的，请联系辅导员先删除今天的填报记录！")>0):
        print("已填报过！")
        MessageSend.send("已填报过！", "已填报过！")
    elif(loginReturnText.find("当前时间不在填报时间范围内！")>0):
        print("当前时间不在填报时间范围内！")
        MessageSend.send("当前时间不在填报时间范围内！", "当前时间不在填报时间范围内！")
    else:
        reportStatusCode, reportReturnText = executeHealthRepoter.report()
        if(reportStatusCode == 200 & reportReturnText.find('填报成功！')>0):
            print("填报成功！")
            MessageSend.send("填报成功！", "填报成功！")
        elif(reportStatusCode == 200 & reportReturnText.find('已经申报成功，请勿重复提交！')>0):
            print("已经申报成功，请勿重复提交！")
            MessageSend.send("已经申报成功，请勿重复提交！", "已经申报成功，请勿重复提交！")
        else: 
            print(reportStatusCode+"\n"+reportReturnText)
            MessageSend.send("出现错误,状态码："+str(reportStatusCode), reportReturnText)
else:
    print(loginAccount+"\n"+loginReturnText)
    MessageSend.send("出现错误,状态码："+str(loginStatusCode), loginReturnText)