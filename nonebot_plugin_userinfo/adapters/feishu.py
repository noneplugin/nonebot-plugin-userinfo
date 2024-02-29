from typing import Optional

from nonebot.log import logger

from ..getter import UserInfoGetter, register_user_info_getter
from ..image_source import ImageUrl
from ..user_info import UserGender, UserInfo

try:
    from nonebot.adapters.feishu import Bot, Event
    from nonebot.adapters.feishu.exception import FeishuAdapterException

    @register_user_info_getter(Bot, Event)
    class Getter(UserInfoGetter[Bot, Event]):
        async def _get_info(self, user_id: str) -> Optional[UserInfo]:
            if user_id in [self.bot.self_id, self.bot.bot_info.open_id]:
                return UserInfo(
                    user_id=self.bot.self_id,
                    user_name=self.bot.bot_info.app_name,
                    user_avatar=ImageUrl(url=str(self.bot.bot_info.avatar_url)),
                )

            info = None

            id_types = ["open_id", "union_id", "user_id"]
            for id_type in id_types:
                params = {"method": "GET", "query": {"user_id_type": id_type}}
                try:
                    resp = await self.bot.call_api(
                        f"contact/v3/users/{user_id}", **params
                    )
                    info = resp["data"]["user"]
                    break
                except FeishuAdapterException as e:
                    logger.warning(f"Error calling contact/v3/users/{user_id}: {e}")
                    continue

            if info:
                gender = info["gender"]
                user_gender = (
                    UserGender.male
                    if gender == 1
                    else UserGender.female
                    if gender == 2
                    else UserGender.unknown
                )
                return UserInfo(
                    user_id=info["open_id"],
                    user_name=info["name"],
                    user_displayname=info.get("nickname"),
                    user_avatar=ImageUrl(url=info["avatar"]["avatar_origin"]),
                    user_gender=user_gender,
                )

except ImportError:
    pass
