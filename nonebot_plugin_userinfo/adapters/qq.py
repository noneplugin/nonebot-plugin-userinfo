from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl, QQAvatarOpenId
from ..user_info import UserInfo

try:
    from nonebot.adapters.qq import (
        Bot,
        C2CMessageCreateEvent,
        Event,
        GroupAtMessageCreateEvent,
        GuildMessageEvent,
    )

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            user = None

            if self.bot.self_id == user_id:
                try:
                    user = await self.bot.me()
                except ActionFailed as e:
                    logger.warning(f"Error calling me: {e}")

            if not user and isinstance(self.event, GuildMessageEvent):
                if self.event.author.id == user_id:
                    user = self.event.author
                else:
                    guild_id = self.event.guild_id
                    try:
                        member = await self.bot.get_member(
                            guild_id=guild_id, user_id=user_id
                        )
                        if member:
                            user = member.user
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_member: {e}")

            if user:
                return UserInfo(
                    user_id=user.id,
                    user_name=user.username or "",
                    user_avatar=ImageUrl(url=user.avatar) if user.avatar else None,
                )

            if isinstance(
                self.event, (C2CMessageCreateEvent, GroupAtMessageCreateEvent)
            ):
                return UserInfo(
                    user_id=user_id,
                    user_name="",
                    user_avatar=QQAvatarOpenId(
                        appid=self.bot.bot_info.id, user_openid=user_id
                    ),
                )

except ImportError:
    pass
