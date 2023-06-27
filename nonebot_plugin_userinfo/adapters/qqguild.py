from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger
from nonebot_plugin_session import SessionLevel

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl
from ..user_info import UserInfo

try:
    from nonebot.adapters.qqguild import Bot, Event, MessageEvent

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            member = None
            user = None

            if self.session.level == SessionLevel.LEVEL3:
                if self.session.id3:
                    try:
                        member = await self.bot.get_member(
                            guild_id=int(self.session.id3), user_id=int(user_id)
                        )
                        if member:
                            user = member.user
                    except ActionFailed as e:
                        logger.warning(f"Error calling get_member: {e}")
                        pass

            if not user:
                if self.bot.self_id == user_id:
                    try:
                        user = await self.bot.me()
                    except ActionFailed as e:
                        logger.warning(f"Error calling me: {e}")
                        pass

                elif (
                    isinstance(self.event, MessageEvent)
                    and self.event.author
                    and str(self.event.author.id) == user_id
                ):
                    user = self.event.author

            if user:
                return UserInfo(
                    user_id=user_id,
                    user_name=user.username or "",
                    user_displayname=member.nick if member else None,
                    user_avatar=ImageUrl(url=user.avatar) if user.avatar else None,
                )

except ImportError:
    pass
