import asyncio
import re

import httpx
from nonebot.log import logger

from .exception import NetworkError


async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=10)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                logger.warning(f"Error downloading {url}, retry {i}/3: {e}")
                await asyncio.sleep(3)
    raise NetworkError(f"{url} 下载失败！")


def check_qq_number(qq: str) -> bool:
    return bool(re.match(r"^\d{5,11}$", qq))
