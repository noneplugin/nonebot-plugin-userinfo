from nonebot import on_command
from nonebot.adapters import Bot, Event

from nonebot_plugin_userinfo import get_user_info

user_info_cmd = on_command("user_info")


@user_info_cmd.handle()
async def handle(bot: Bot, event: Event):
    user_info = await get_user_info(bot, event, event.get_user_id())
    await user_info_cmd.send(user_info) # type: ignore