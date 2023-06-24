import hashlib

import emoji
from pydantic import BaseModel, validator
from strenum import StrEnum

from .utils import download_url


class ImageSource(BaseModel):
    async def get_image(self) -> bytes:
        raise NotImplementedError


class ImageUrl(ImageSource):
    url: str

    async def get_image(self) -> bytes:
        return await download_url(self.url)


class EmojiStyle(StrEnum):
    Apple = "apple"
    Google = "google"
    Microsoft = "microsoft"
    Samsung = "samsung"
    WhatsApp = "whatsapp"
    Twitter = "twitter"
    Facebook = "facebook"
    Messenger = "messenger"
    JoyPixels = "joypixels"
    OpenMoji = "openmoji"
    EmojiDex = "emojidex"
    LG = "lg"
    HTC = "htc"
    Mozilla = "mozilla"


class Emoji(ImageSource):
    data: str

    @validator("data")
    def check_emoji(cls, value: str) -> str:
        if not emoji.is_emoji(value):
            raise ValueError("Not a emoji")
        return value

    def get_url(self, style: EmojiStyle = EmojiStyle.Apple) -> str:
        return f"https://emojicdn.elk.sh/{self.data}?style={style}"

    async def get_image(self, style: EmojiStyle = EmojiStyle.Apple) -> bytes:
        return await download_url(self.get_url(style))


class QQAvatar(ImageSource):
    qq: int

    async def get_image(self) -> bytes:
        url = f"http://q1.qlogo.cn/g?b=qq&nk={self.qq}&s=640"
        data = await download_url(url)
        if hashlib.md5(data).hexdigest() == "acef72340ac0e914090bd35799f5594e":
            url = f"http://q1.qlogo.cn/g?b=qq&nk={self.qq}&s=100"
            data = await download_url(url)
        return data


class TelegramFile(ImageSource):
    token: str
    file_path: str
    api_server: str = "https://api.telegram.org/"

    def get_url(self) -> str:
        return f"{self.api_server}file/bot{self.token}/{self.file_path}"

    async def get_image(self) -> bytes:
        return await download_url(self.get_url())
