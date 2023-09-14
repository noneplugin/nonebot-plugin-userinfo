from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import QQAvatar
from ..user_info import UserGender, UserInfo

try:
    from nonebot.adapters.red import Bot
    from nonebot.adapters.red.event import Event, MessageEvent

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            if user_id == self.bot.self_id:
                try:
                    profile = await self.bot.get_self_profile()
                except ActionFailed as e:
                    logger.warning(f"Error calling get_self_profile: {e}")
                    return
                qq = profile.uin
                sex = profile.sex
                gender = (
                    UserGender.male
                    if sex == 1
                    else UserGender.female
                    if sex == 2
                    else UserGender.unknown
                )
                return UserInfo(
                    user_id=qq,
                    user_name=profile.nick,
                    user_avatar=QQAvatar(qq=int(qq)),
                    user_gender=gender,
                )

            if (
                isinstance(self.event, MessageEvent)
                and self.event.senderUin
                and user_id == self.event.senderUin
            ):
                qq = self.event.senderUin
                return UserInfo(
                    user_id=qq,
                    user_name=self.event.sendNickName,
                    user_displayname=self.event.sendMemberName,
                    user_avatar=QQAvatar(qq=int(qq)),
                )

except ImportError:
    pass
