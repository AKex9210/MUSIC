import os
import re

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from AnonXMusic import app
from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def clear(text):
    list = text.split(" ")
    title = ""
    for i in list:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = ""
            try:
                duration = result[""]
            except:
                duration = ""
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result[""][""]
            except:
                views = ""
            try:
                channel = result[""][""]
            except:
                channel = ""

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(0))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(1.00)
        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("UnxMusic/assets/font2.ttf", 30)
        font = ImageFont.truetype("UnxMusic/assets/font.ttf", 30)
        draw.text(
            (55, 560),
            f"{channel} {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (57, 600),
            clear("‎ "),
            (255, 255, 255),
            font=font,
        )
        draw.text(
            (1185, 685),
            f"{duration[:23]}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
