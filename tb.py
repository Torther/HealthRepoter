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

print(loginId[0])
print(loginPwd[0])
print(householdRegister[0])
print(phoneNumber[0])
print(currentLocation[0])

r = requests.get("http://www.wzpt.edu.cn/")
print(r.text)

print("结束")
