<div align="center">

  <a href="https://nonebot.dev/">
    <img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot">
  </a>

# nonebot-plugin-userinfo

_✨ [Nonebot2](https://github.com/nonebot/nonebot2) 用户信息获取插件 ✨_

<p align="center">
  <img src="https://img.shields.io/github/license/noneplugin/nonebot-plugin-userinfo" alt="license">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/nonebot-2.0.0+-red.svg" alt="NoneBot">
  <a href="https://pypi.org/project/nonebot-plugin-userinfo">
    <img src="https://badgen.net/pypi/v/nonebot-plugin-userinfo" alt="pypi">
  </a>
</p>

</div>

多平台的用户信息获取插件，可以获取用户名、用户头像等信息

可以获取的信息：

| 字段             | 类型                    | 说明     | 默认值      | 备注                                                                                                                                                        |
| ---------------- | ----------------------- | -------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| user_id          | `str`                   | 用户 id  |             |                                                                                                                                                             |
| user_name        | `str`                   | 用户名   |             |                                                                                                                                                             |
| user_displayname | `Optional[str]`         | 用户昵称 | `None`      |                                                                                                                                                             |
| user_remark      | `Optional[str]`         | 用户备注 | `None`      |                                                                                                                                                             |
| user_avatar      | `Optional[ImageSource]` | 用户头像 | `None`      | [ImageSource](https://github.com/noneplugin/nonebot-plugin-userinfo/blob/main/nonebot_plugin_userinfo/image_source.py) 可通过 `get_image` 获取 `bytes` 结果 |
| user_gender      | `str`                   | 用户性别 | `"unknown"` |                                                                                                                                                             |

### 安装

- 使用 nb-cli

```
nb plugin install nonebot_plugin_userinfo
```

- 使用 pip

```
pip install nonebot_plugin_userinfo
```

### 使用

```python
from nonebot_plugin_userinfo import get_user_info

@matcher.handle()
async def handle(bot: Bot, event: Event):
    user_info = get_user_info(bot, event, event.get_user_id())  # 获取当前事件主体用户的信息
```

可以用依赖注入的方式使用：

```python
from nonebot_plugin_userinfo import EventUserInfo, UserInfo

@matcher.handle()
async def handle(user_info: UserInfo = EventUserInfo()):  # 获取当前事件主体用户的信息
    pass
```

```python
from nonebot_plugin_userinfo import BotUserInfo, UserInfo

@matcher.handle()
async def handle(user_info: UserInfo = BotUserInfo()):  # 获取Bot用户信息
    pass
```

### 支持的 adapter

- [x] OneBot v11
- [x] OneBot v12
- [x] Console
- [x] Kaiheila
- [x] Telegram
- [x] Feishu
- [x] RedProtocol
- [x] Discord
- [x] DoDo
- [x] Satori
- [x] QQ

### 鸣谢

- [nonebot-plugin-send-anything-anywhere](https://github.com/felinae98/nonebot-plugin-send-anything-anywhere) 项目的灵感来源以及部分实现的参考
- [uy/sun](https://github.com/he0119) 感谢歪日佬的技术支持
