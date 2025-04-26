# services/membership.py
from pyrogram import Client
from config import config
from services.db import list_groups

async def add_members():
    app = Client(
        config.SESSION_NAME,
        api_id=config.API_ID,
        api_hash=config.API_HASH
    )
    await app.start()
    for chat_id, dst in list_groups():
        async for member in app.get_chat_members(chat_id):
            await app.add_chat_members(dst, [member.user.id])
    await app.stop()