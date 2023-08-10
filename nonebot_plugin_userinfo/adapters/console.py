from typing import Optional

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import Emoji
from ..user_info import UserInfo

try:
    from nonebot.adapters.console import Bot, Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            user = self.event.user
            if user_id in [user.id, user.nickname]:
                return UserInfo(
                    user_id=user.nickname,
                    user_name=user.nickname,
                    user_avatar=Emoji(data=user.avatar),
                )

except ImportError:
    pass
