import hashlib
from pathlib import Path

import anyio
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

    async def get_image(self, style: EmojiStyle = EmojiStyle.Apple) -> bytes:
        url = f"https://emojicdn.elk.sh/{self.data}?style={style}"
        return await download_url(url)


class QQAvatar(ImageSource):
    qq: int

    async def get_image(self) -> bytes:
        url = f"http://q1.qlogo.cn/g?b=qq&nk={self.qq}&s=640"
        data = await download_url(url)
        if hashlib.md5(data).hexdigest() == "acef72340ac0e914090bd35799f5594e":
            url = f"http://q1.qlogo.cn/g?b=qq&nk={self.qq}&s=100"
            data = await download_url(url)
        return data


class QQAvatarOpenId(ImageSource):
    appid: str
    user_openid: str

    async def get_image(self) -> bytes:
        url = f"https://q.qlogo.cn/qqapp/{self.appid}/{self.user_openid}/100"
        return await download_url(url)


class TelegramFile(ImageSource):
    token: str
    file_path: str

    async def get_image(self, api_server: str = "https://api.telegram.org/") -> bytes:
        if Path(self.file_path).exists():
            return await anyio.Path(self.file_path).read_bytes()
        url = f"{api_server}file/bot{self.token}/{self.file_path}"
        return await download_url(url)


class DiscordImageFormat(StrEnum):
    JPEG = "jpeg"
    PNG = "png"
    WebP = "webp"
    GIF = "gif"
    Lottie = "json"


class DiscordUserAvatar(ImageSource):
    # https://discord.com/developers/docs/reference#image-formatting

    user_id: int
    image_hash: str

    async def get_image(
        self,
        base_url: str = "https://cdn.discordapp.com/",
        image_format: DiscordImageFormat = DiscordImageFormat.PNG,
        image_size: int = 1024,
    ) -> bytes:
        url = f"{base_url}avatars/{self.user_id}/{self.image_hash}.{image_format}?size={image_size}"
        return await download_url(url)
