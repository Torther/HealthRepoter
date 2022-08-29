# 温州职业技术学院健康填报工具

## 使用方法

- Fork 本仓库
- 打开 Fork 的仓库的 `Settings` -> `Secrets` -> `Actions`
    - 添加以下字段，并填相应的值
        - LOGIN_ACCOUNT
        - LOGIN_PASSWORD
        - HOUSEHOLD_REGISTER
        - PHONE_NUMBER
        - CURRENT_LOCATION
        - SERVERCHAN_KEY

| 字段 | 说明 |
| ---- |-------------|
| LOGIN_ACCOUNT | 学号 |
| LOGIN_PASSWORD | 密码 |
| HOUSEHOLD_REGISTER | 户口所在地 |
| PHONE_NUMBER | 联系电话 |
| CURRENT_LOCATION | 现所在地 |
| SERVERCHAN_KEY | Server 酱 Key |

- 启用 Actions

## 提示

- 打卡调用的是学校公开的 API <https://info2.webvpn.wzvtc.cn/supply/index.jsp>
