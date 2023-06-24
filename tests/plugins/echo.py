from nonebot import on_command
from nonebot.adapters import Bot, Event

from nonebot_plugin_userinfo import BotUserInfo, EventUserInfo, UserInfo, get_user_info

user_info_cmd = on_command("user_info")


@user_info_cmd.handle()
async def user_info_handle(bot: Bot, event: Event):
    user_info = await get_user_info(bot, event, event.get_user_id(), use_cache=False)
    await user_info_cmd.send("", user_info=user_info)


user_info_depends_cmd = on_command("user_info_depends")


@user_info_depends_cmd.handle()
async def user_info_depends_handle(
    user_info: UserInfo = EventUserInfo(use_cache=False),
):
    await user_info_depends_cmd.send("", user_info=user_info)


bot_user_info_cmd = on_command("bot_user_info")


@bot_user_info_cmd.handle()
async def handle(user_info: UserInfo = BotUserInfo(use_cache=False)):  # 获取Bot用户信息
    await bot_user_info_cmd.send("", user_info=user_info)
