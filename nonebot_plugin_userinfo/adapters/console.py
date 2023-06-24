from typing import Optional

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import Emoji
from ..user_info import UserInfo

try:
    from nonebot.adapters.console import Bot, Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            if user_id in [self.event.user.id, self.event.user.nickname]:
                user = self.event.user
                return UserInfo(
                    user_id=user_id,
                    user_name=user.nickname,
                    user_avatar=Emoji(data=user.avatar),
                )

            if user_id in [self.bot.info.id, self.bot.info.nickname]:
                info = self.bot.info
                return UserInfo(
                    user_id=user_id,
                    user_name=info.nickname,
                    user_avatar=Emoji(data=info.avatar),
                )

except ImportError:
    pass
