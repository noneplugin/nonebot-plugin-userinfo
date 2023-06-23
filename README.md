<div align="center">

  <a href="https://v2.nonebot.dev/">
    <img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot">
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

- [ ] TODO


### 鸣谢

- [nonebot-plugin-send-anything-anywhere](https://github.com/felinae98/nonebot-plugin-send-anything-anywhere) 项目的灵感来源以及部分实现的参考
- [uy/sun](https://github.com/he0119) 感谢歪日佬的技术支持
