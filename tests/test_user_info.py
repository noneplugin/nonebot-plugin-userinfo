from datetime import datetime

import pytest
from nonebot.adapters.console import Bot, Message, MessageEvent, Robot, User
from nonebug import App


@pytest.mark.asyncio
async def test_user_info(app: App):
    from nonebot_plugin_userinfo import Emoji, UserInfo
    from tests.plugins.echo import user_info_cmd

    event = MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message("/user_info"),
        user=User(id="123456789", avatar="🤗", nickname="MyUser"),
    )

    user_info = UserInfo(
        user_id="MyUser",
        user_name="MyUser",
        user_displayname=None,
        user_remark=None,
        user_avatar=Emoji(data="🤗"),
        user_gender="unknown",
    )

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot)
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)


@pytest.mark.asyncio
async def test_user_info_depends(app: App):
    from nonebot_plugin_userinfo import Emoji, UserInfo
    from tests.plugins.echo import user_info_depends_cmd

    event = MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message("/user_info_depends"),
        user=User(id="123456789", avatar="🤗", nickname="MyUser"),
    )

    user_info = UserInfo(
        user_id="MyUser",
        user_name="MyUser",
        user_displayname=None,
        user_remark=None,
        user_avatar=Emoji(data="🤗"),
        user_gender="unknown",
    )

    async with app.test_matcher(user_info_depends_cmd) as ctx:
        bot = ctx.create_bot(base=Bot)
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)


@pytest.mark.asyncio
async def test_bot_user_info(app: App):
    from nonebot_plugin_userinfo import Emoji, UserInfo
    from tests.plugins.echo import bot_user_info_cmd

    event = MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message("/bot_user_info"),
        user=User(id="123456789", avatar="🤗", nickname="MyUser"),
    )

    user_info = UserInfo(
        user_id="test",
        user_name="Bot",
        user_displayname=None,
        user_remark=None,
        user_avatar=Emoji(data="🤖"),
        user_gender="unknown",
    )

    async with app.test_matcher(bot_user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot)
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, user_info=user_info)
