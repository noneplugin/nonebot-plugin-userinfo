from nonebot import on_command
from nonebot.adapters import Bot, Event, Message
from nonebot.params import CommandArg

from nonebot_plugin_userinfo import BotUserInfo, EventUserInfo, UserInfo, get_user_info

user_info_cmd = on_command("user_info")


@user_info_cmd.handle()
async def _(bot: Bot, event: Event, arg: Message = CommandArg()):
    user_id = arg.extract_plain_text().strip()
    if not user_id:
        user_id = event.get_user_id()
    user_info = await get_user_info(bot, event, user_id, use_cache=False)
    await user_info_cmd.send("", user_info=user_info)


user_info_depends_cmd = on_command("user_info_depends")


@user_info_depends_cmd.handle()
async def _(
    user_info: UserInfo = EventUserInfo(use_cache=False),
):
    await user_info_depends_cmd.send("", user_info=user_info)


bot_user_info_cmd = on_command("bot_user_info")


@bot_user_info_cmd.handle()
async def _(user_info: UserInfo = BotUserInfo(use_cache=False)):  # 获取Bot用户信息
    await bot_user_info_cmd.send("", user_info=user_info)
