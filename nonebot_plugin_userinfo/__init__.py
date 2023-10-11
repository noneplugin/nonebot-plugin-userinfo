from nonebot.plugin import PluginMetadata

from . import adapters
from .getter import BotUserInfo, EventUserInfo, get_user_info
from .image_source import ImageSource
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
        # "~qqguild",
        "~telegram",
        "~feishu",
        "~red",
        "~discord",
    },
)
