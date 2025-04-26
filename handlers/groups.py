# handlers/groups.py
from aiogram import Router, types
from aiogram.filters import Text
from services.db import add_group, list_groups

router = Router()

@router.message(Text(equals='Добавить группу'))
async def cmd_add_group(msg: types.Message):
    await msg.answer("Введите chat_id и destination_chat_id через пробел:")

@router.message(Text(regexp=r'^\d+\s+\d+$'))
async def handle_group_input(msg: types.Message):
    parts = msg.text.split()
    chat_id, dest_id = map(int, parts)
    add_group(chat_id, dest_id)
    await msg.answer(f"Группа добавлена: {chat_id} → {dest_id}")

@router.message(Text(equals='Просмотреть список групп'))
async def cmd_list_groups(msg: types.Message):
    rows = list_groups()
    if not rows:
        await msg.answer("Нет групп в БД.")
    else:
        lines = [f"{cid} → {dst}" for cid, dst in rows]
        await msg.answer("Список групп:\n" + "\n".join(lines))