from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.models import async_session, Category, Item
from sqlalchemy import select

# Меню
btn_menu = [
    [InlineKeyboardButton(text='Каталог🛍', callback_data='catalog')],
    [InlineKeyboardButton(text='Связь с нами📞', callback_data='call')],
    [InlineKeyboardButton(text='Корзина 🛒', callback_data='cart')],
]

keyboard_menu = InlineKeyboardMarkup(inline_keyboard=btn_menu)

async def categories_kb():
    async with async_session() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        
        builder = InlineKeyboardBuilder()
        
        for category in categories:
            builder.button(
                text=category.name,
                callback_data=f"category_{category.id}"
            )
            
        builder.button(
            text="⬅️ Назад",
            callback_data="back_to_menu"
        )

        builder.adjust(1)
        return builder.as_markup()

async def items_kb(category_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Item).where(Item.category == category_id))
        items = result.scalars().all()
        
        builder = InlineKeyboardBuilder()
        
        for item in items:
            builder.button(
                text=f"{item.name} - {item.price}₽",
                callback_data=f"item_{item.id}"
            )
        
        builder.button(
            text="⬅️ Назад",
            callback_data="back_to_cats"
        )

        
        
        builder.adjust(1)
        return builder.as_markup()

async def item_detail_kb(item_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️ Назад",
        callback_data=f"back_to_items_{item_id}"
    )

    builder.button(
        text="🛒В корзину",
        callback_data="buy_cart"
    )
    return builder.as_markup()