from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl
from ..user_info import UserInfo

try:
    from nonebot.adapters.qqguild import (
        Bot,
        DirectMessageCreateEvent,
        Event,
        MessageAuditEvent,
        MessageEvent,
        MessageReactionEvent,
    )

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            member = None
            user = None

            if isinstance(
                self.event,
                (
                    MessageEvent,
                    MessageAuditEvent,
                    MessageReactionEvent,
                ),
            ) and not isinstance(self.event, DirectMessageCreateEvent):
                if guild_id := self.event.guild_id:
                    try:
                        member = await self.bot.get_member(
                            guild_id=int(guild_id), user_id=int(user_id)
                        )
                        if member:
                            user = member.user
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_member: {e}")

            if not user:
                if self.bot.self_id == user_id:
                    try:
                        user = await self.bot.me()
                    except ActionFailed as e:
                        logger.warning(f"Error calling me: {e}")

                elif (
                    isinstance(self.event, MessageEvent)
                    and self.event.author
                    and str(self.event.author.id) == user_id
                ):
                    user = self.event.author

            if user:
                return UserInfo(
                    user_id=str(user.id) if user.id else user_id,
                    user_name=user.username or "",
                    user_displayname=member.nick if member else None,
                    user_avatar=ImageUrl(url=user.avatar) if user.avatar else None,
                )

except ImportError:
    pass
