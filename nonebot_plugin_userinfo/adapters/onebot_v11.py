from typing import Optional

from nonebot.exception import ActionFailed
from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import QQAvatar
from ..user_info import UserGender, UserInfo
from ..utils import check_qq_number

try:
    from nonebot.adapters.onebot.v11 import (
        Bot,
        Event,
        GroupAdminNoticeEvent,
        GroupBanNoticeEvent,
        GroupDecreaseNoticeEvent,
        GroupIncreaseNoticeEvent,
        GroupMessageEvent,
        GroupRecallNoticeEvent,
        GroupRequestEvent,
        GroupUploadNoticeEvent,
    )

    def _sex_to_gender(sex: Optional[str]) -> UserGender:
        return (
            UserGender.male
            if sex == "male"
            else UserGender.female
            if sex == "female"
            else UserGender.unknown
        )

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            info = None

            if isinstance(
                self.event,
                (
                    GroupAdminNoticeEvent,
                    GroupBanNoticeEvent,
                    GroupDecreaseNoticeEvent,
                    GroupIncreaseNoticeEvent,
                    GroupMessageEvent,
                    GroupRecallNoticeEvent,
                    GroupRequestEvent,
                    GroupUploadNoticeEvent,
                ),
            ):
                try:
                    info = await self.bot.get_group_member_info(
                        group_id=self.event.group_id, user_id=int(user_id)
                    )
                except ActionFailed as e:
                    logger.warning(f"Error calling get_group_member_info: {e}")

            if not info:
                try:
                    info = await self.bot.get_stranger_info(user_id=int(user_id))
                except ActionFailed as e:
                    logger.warning(f"Error calling get_stranger_info failed: {e}")

            if info:
                qq = info["user_id"]
                sex = info.get("sex")
                return UserInfo(
                    user_id=str(qq),
                    user_name=info.get("nickname", ""),
                    user_displayname=info.get("card"),
                    user_avatar=QQAvatar(qq=qq),
                    user_gender=_sex_to_gender(sex),
                )

            if check_qq_number(user_id):
                return UserInfo(
                    user_id=user_id,
                    user_name="",
                    user_avatar=QQAvatar(qq=int(user_id)),
                )

except ImportError:
    pass
