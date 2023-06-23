from typing import Optional

from ..getter import UserInfoGetter, register_user_info_getter
from ..user_info import UserInfo

try:
    from nonebot.adapters.console import Bot, Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            if user_id in [self.event.user.id, self.event.user.nickname]:
                return UserInfo(user_id=user_id, user_name=self.event.user.nickname)

            if user_id in [self.bot.info.id, self.bot.info.nickname]:
                return UserInfo(user_id=user_id, user_name=self.bot.info.nickname)

except ImportError:
    pass
