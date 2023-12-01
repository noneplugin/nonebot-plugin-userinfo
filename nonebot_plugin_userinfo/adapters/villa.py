from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl
from ..user_info import UserInfo

try:
    from nonebot.adapters.villa import Bot, Event

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            template = self.event.robot.template
            if template.id == user_id:
                return UserInfo(
                    user_id=template.id,
                    user_name=template.name,
                    user_avatar=ImageUrl(url=template.icon),
                )

            if not user_id.isdigit():
                return

            try:
                user = await self.bot.get_member(
                    villa_id=self.event.robot.villa_id, uid=int(user_id)
                )
                return UserInfo(
                    user_id=str(user.basic.uid),
                    user_name=user.basic.nickname,
                    user_avatar=ImageUrl(url=user.basic.avatar_url),
                )
            except ActionFailed as e:
                logger.warning(f"Error calling get_member: {e}")

except ImportError:
    pass
