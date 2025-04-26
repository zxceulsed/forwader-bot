# handlers/duplication.py
import asyncio
from aiogram import Router, types
from aiogram.filters import Text
from services.duplicator import pyrogram_worker, stop_worker

router = Router()

@router.message(Text(equals='Начать дублирование контента'))
async def start_dup(msg: types.Message):
    await msg.answer("Запускаю дублирование контента...")
    asyncio.create_task(pyrogram_worker())

@router.message(Text(equals='Остановить дублирование'))
async def stop_dup(msg: types.Message):
    stop_worker()
    await msg.answer("Останавливаю дублирование контента.")