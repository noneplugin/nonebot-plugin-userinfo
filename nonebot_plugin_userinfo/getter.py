from typing import Generic, List, NamedTuple, Optional, Type, TypeVar

from cachetools import TTLCache
from nonebot.adapters import Bot, Event
from nonebot.params import Depends

from .user_info import UserInfo

_user_info_cache = TTLCache(maxsize=float("inf"), ttl=10)

B = TypeVar("B", bound=Bot)
E = TypeVar("E", bound=Event)


class UserInfoGetter(Generic[B, E]):
    def __init__(self, bot: B, event: E):
        self.bot = bot
        self.event = event

    async def _get_info(self, user_id: str) -> Optional[UserInfo]:
        raise NotImplementedError

    async def get_info(
        self, user_id: str, use_cache: bool = True
    ) -> Optional[UserInfo]:
        if use_cache:
            try:
                session_id = self.event.get_session_id()
            except NotImplementedError:
                session_id = ""
            id = f"{session_id}_{user_id}"
            if id in _user_info_cache:
                return _user_info_cache[id]
            info = await self._get_info(user_id)
            if info:
                _user_info_cache[id] = info
            return info
        else:
            return await self._get_info(user_id)


class UserInfoGetterTuple(NamedTuple):
    bot: Type[Bot]
    event: Type[Event]
    getter: Type[UserInfoGetter]


_user_info_getters: List[UserInfoGetterTuple] = []


def register_user_info_getter(bot: Type[Bot], event: Type[Event]):
    def wrapper(getter: Type[UserInfoGetter]):
        _user_info_getters.append(UserInfoGetterTuple(bot, event, getter))
        return getter

    return wrapper


async def get_user_info(
    bot: Bot, event: Event, user_id: str, use_cache: bool = True
) -> Optional[UserInfo]:
    for getter_tuple in _user_info_getters:
        if isinstance(bot, getter_tuple.bot) and isinstance(event, getter_tuple.event):
            return await getter_tuple.getter(bot, event).get_info(
                user_id, use_cache=use_cache
            )


def EventUserInfo(use_cache: bool = True):
    async def dependency(bot: Bot, event: Event) -> Optional[UserInfo]:
        return await get_user_info(bot, event, event.get_user_id(), use_cache=use_cache)

    return Depends(dependency)


def BotUserInfo(use_cache: bool = True):
    async def dependency(bot: Bot, event: Event) -> Optional[UserInfo]:
        return await get_user_info(bot, event, bot.self_id, use_cache=use_cache)

    return Depends(dependency)
