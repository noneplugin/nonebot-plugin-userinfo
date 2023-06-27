from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_session")

from . import adapters
from .getter import BotUserInfo, EventUserInfo, get_user_info
from .image_source import Emoji, ImageSource, ImageUrl, QQAvatar, TelegramFile
from .user_info import UserInfo

__plugin_meta__ = PluginMetadata(
    name="用户信息",
    description="多平台的用户信息获取插件",
    usage="请参考文档",
    type="library",
    homepage="https://github.com/noneplugin/nonebot-plugin-userinfo",
    supported_adapters={
        "~onebot.v11",
        "~onebot.v12",
        "~console",
        "~kaiheila",
        "~qqguild",
        "~telegram",
    },
)
