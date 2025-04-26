# handlers/messages.py
from aiogram import Router, types
from aiogram.filters import Text
from services.db import get_last_message, update_last_message, list_groups
from config import config
from pyrogram import Client

router = Router()

@router.message(Text(equals='Проверить сообщения'))
async def cmd_check(msg: types.Message):
    await msg.answer("Проверка новых сообщений...")
    app = Client(
        config.SESSION_NAME,
        api_id=config.API_ID,
        api_hash=config.API_HASH
    )
    await app.start()
    for chat_id, dst in list_groups():
        last_msg = get_last_message(chat_id)
        new_msgs = []
        async for m in app.get_chat_history(chat_id):
            if m.text:
                if last_msg and m.text == last_msg:
                    break
                new_msgs.append(m.text)
            else:
                if m.photo:
                    await app.send_photo(dst, m.photo.file_id, caption=m.caption)
                elif m.document:
                    await app.send_document(dst, m.document.file_id, caption=m.caption)
                elif m.video:
                    await app.send_video(dst, m.video.file_id, caption=m.caption)
        for text in reversed(new_msgs):
            await app.send_message(dst, text)
        if new_msgs:
            update_last_message(chat_id, new_msgs[0])
    await app.stop()
    await msg.answer("Проверка завершена.")