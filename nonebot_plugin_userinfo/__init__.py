from nonebot.plugin import PluginMetadata

from . import adapters as adapters
from .getter import BotUserInfo as BotUserInfo
from .getter import EventUserInfo as EventUserInfo
from .getter import get_user_info as get_user_info
from .image_source import ImageSource as ImageSource
from .user_info import UserGender as UserGender
from .user_info import UserInfo as UserInfo

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
        "~telegram",
        "~feishu",
        "~red",
        "~discord",
        "~dodo",
        "~satori",
        "~qq",
    },
)
