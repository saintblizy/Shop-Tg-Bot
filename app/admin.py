from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.models import async_session, Category, Item
from sqlalchemy import select


btn_admin = [
    [InlineKeyboardButton(text='Каталог🛍', callback_data='catalog')],
    [InlineKeyboardButton(text='Связь с нами📞', callback_data='call')],
    [InlineKeyboardButton(text='Корзина 🛒', callback_data='cart')],
    [InlineKeyboardButton(text='Админ панель💻', callback_data='for_admin')],
]

keyboard_admin = InlineKeyboardMarkup(inline_keyboard=btn_admin)


btn_for_admin = [
    [InlineKeyboardButton(text='Добавить категорию📝', callback_data='add_category')],
    [InlineKeyboardButton(text='Добавить товар👟', callback_data='add_product')],
    [InlineKeyboardButton(text='Убрать категорию🗑', callback_data='del_category')],
    [InlineKeyboardButton(text='Убрать товар🗑', callback_data='del_product')],
    [InlineKeyboardButton(text='Узнать ID товара🔎', callback_data='search_id_item')],
    [InlineKeyboardButton(text='Узнать ID категории🔎', callback_data='search_id_category')],
    [InlineKeyboardButton(text='Назад⬅️', callback_data='back_to_menu_admin')]

]

keyboard_for_admin = InlineKeyboardMarkup(inline_keyboard=btn_for_admin)
