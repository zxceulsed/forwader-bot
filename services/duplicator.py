# services/duplicator.py
from pyrogram import Client
from pyrogram.types import Message, InputMediaPhoto, InputMediaDocument, InputMediaVideo
from config import config
from services.db import list_groups

async def pyrogram_worker():
    app = Client(
        config.SESSION_NAME,
        api_id=config.API_ID,
        api_hash=config.API_HASH
    )

    @app.on_message()
    async def handler(client: Client, message: Message):
        for chat_id, dst in list_groups():
            if message.chat.id == chat_id:
                text = message.text or ''
                if text:
                    await client.send_message(dst, text)
                else:
                    media = _extract_media(message)
                    if media:
                        await client.send_media_group(dst, media=media)

    await app.start()
    # await app.idle()  # если нужно остается активным


def _extract_media(message: Message) -> list:
    items = []
    caption = message.caption
    if message.photo:
        items.append(InputMediaPhoto(message.photo.file_id, caption=caption))
    elif message.document:
        items.append(InputMediaDocument(message.document.file_id, caption=caption))
    elif message.video:
        items.append(InputMediaVideo(message.video.file_id, caption=caption))
    return items