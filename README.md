# 温职打卡脚本

1. Fork->Settings->Secrets
    - 添加以下字段
        - LOGIN_ID
        - LOGIN_PWD
        - HOUSEHOLD_REGISTER
        - PHONE_NUMBER
        - CURRENT_LOCATION
1. 启用Actions

| 字段 | 说明 |
| ---- | ---- |
| LOGIN_ID | 学号 |
| LOGIN_PWD | 密码 |
| HOUSEHOLD_REGISTER | 户口所在地 |
| PHONE_NUMBER | 联系电话 |
| CURRENT_LOCATION | 现所在地 |

PS:打卡调用的是学校公开的API https://info2.webvpn.wzvtc.cn/supply/index.jsp
