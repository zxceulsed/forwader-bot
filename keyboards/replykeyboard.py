# keyboards/replykeyboard.py
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from config import config


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='Добавить группу')
    builder.button(text='Просмотреть список групп')
    builder.button(text='Начать дублирование контента')
    builder.button(text='Добавить в мою группу')
    builder.button(text='Проверить сообщения')
    builder.adjust(*config.ROWS)
    return builder.as_markup(resize_keyboard=True)