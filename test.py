import os

# 学号
loginId = os.environ["LOGIN_ID"]
# 密码
loginPwd = os.environ["LOGIN_PWD"]
# 户籍
householdRegister = os.environ["HOUSEHOLD_REGISTER"]
# 手机号码https://github.com/luoyikuan/wzpt_tb/blob/main/test.py
phoneNumber = os.environ["PHONE_NUMBER"]
# 当前位置
currentLocation = os.environ["CURRENT_LOCATION"]

print(loginId)
print(loginPwd)
print(householdRegister)
print(phoneNumber)
print(currentLocation)
