from datetime import datetime

import pytest
from nonebot.adapters.console import Bot, Message, MessageEvent, User
from nonebug import App


@pytest.mark.asyncio
async def test_get_plugin(app:App):
    from tests.plugins.echo import user_info_cmd

    event = MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message("/user_info"),
        user=User(id="123456789"),
    )

    async with app.test_matcher(user_info_cmd) as ctx:
        bot = ctx.create_bot(base=Bot)
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, None, True) # type: ignore