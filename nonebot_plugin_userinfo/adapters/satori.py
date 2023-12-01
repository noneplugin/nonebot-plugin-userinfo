from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl
from ..user_info import UserInfo

try:
    from nonebot.adapters.satori import Bot
    from nonebot.adapters.satori.event import Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            user = None

            if self.event.user and self.event.user.id == user_id:
                user = self.event.user

            if not user and self.bot.self_info.id == user_id:
                user = self.bot.self_info

            if not user:
                try:
                    user = await self.bot.user_get(user_id=user_id)
                except ActionFailed as e:
                    logger.warning(f"Error calling user_get: {e}")

            if user:
                user_name = user.name or user.nick
                if user_name:
                    return UserInfo(
                        user_id=user.id,
                        user_name=user_name,
                        user_displayname=user.nick,
                        user_avatar=ImageUrl(url=user.avatar) if user.avatar else None,
                    )

except ImportError:
    pass
