from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.database.models import Add_Category, Add_Product, Del_Category, Del_Product, CatName, ItemName

from app.bot_instance import bot
from app.keyboards import keyboard_menu, categories_kb, items_kb, item_detail_kb
import app.database.requests as rq

from app.admin import keyboard_admin, keyboard_for_admin

import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_ID=str(os.getenv('ADMIN_ID'))

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await rq.set_user(message.from_user.id)
    photo = FSInputFile('D:/python/Shop-Tg-Bot/app/img/logo.png')
    telegram_id = str(message.from_user.id)
    if telegram_id == ADMIN_ID:
        keyboard = keyboard_admin
    else:
        keyboard = keyboard_menu
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption='Приветствую! Ты попал в онлайн магазин кроссовок!',
        reply_markup=keyboard
    )

@router.callback_query(F.data == 'add_category')
async def cq_add_category(callback_query: types.CallbackQuery, state: FSMContext):


@router.callback_query(F.data == 'for_admin')
async def for_admin(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    photo = FSInputFile('D:/python/Shop-Tg-Bot/app/img/logo.png')
    await bot.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=photo,
        caption='Админ панель',
        reply_markup=keyboard_for_admin
    )

@router.callback_query(F.data == 'search_id_category')
async def search_id_category(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите имя категории')
    await state.set_data({})
    await state.set_state(CatName.name)

@router.message(CatName.name)
async def process_item(message: types.Message, state: FSMContext):
    category_name = message.text
    id = await rq.get_id_category(category_name)
    if not id:
        await message.answer(f'Ошибка! {category_name} не найдено')
    else:
        await message.answer(f'🔎ID категории {category_name}: {id}')
        await state.clear()

@router.callback_query(F.data == 'add_product')
async def callback_add_product(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите название товара')
    await state.set_state(Add_Product.name)

@router.message(Add_Product.name)
async def add_item_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите цену товара')
    await state.set_state(Add_Product.price)

@router.message(Add_Product.price)
async def add_item_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await message.answer('Введите описание товара')
        await state.set_state(Add_Product.description)
    except ValueError:
        await message.answer('Пожалуйста, введите корректную цену (число)')

@router.message(Add_Product.description)
async def add_item_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите название категории товара')
    await state.set_state(Add_Product.category)

@router.message(Add_Product.category)
async def add_item_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:

        category_id = await rq.get_id_category(message.text)
        if not category_id:
            await message.answer(f'Категория "{message.text}" не найдена')
            return
            
        await rq.add_item(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            category=category_id
        )
        await message.answer(f'Товар "{data["name"]}" успешно добавлен!')
    except Exception as e:
        await message.answer(f'Ошибка при добавлении товара: {str(e)}')
    finally:
        await state.clear()

@router.callback_query(F.data == 'search_id_item')
async def search_id_item(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите имя товара')
    await state.set_data({})
    await state.set_state(ItemName.name)

@router.message(ItemName.name)
async def id_item(message: types.Message, state: FSMContext):
    item_name = message.text
    id = await rq.get_id_item(item_name)
    if not id:
        await message.answer(f'Ошибка! {item_name} не найдено')
    else:
        await message.answer(f'🔎ID товара {item_name}: {id}')
        await state.clear()


@router.callback_query(F.data == 'del_product')
async def del_item(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите название предмета')
    await state.set_data({})
    await state.set_state(Del_Product.product_name)

@router.message(Del_Product.product_name)
async def process_item(message: types.Message, state: FSMContext):
    item_name = message.text.strip()

    item = await rq.get_items_by_name(item_name)

    if not item:
        await message.answer(f"Кроссовки '{item_name}' не найдены")
        await state.clear()
        return
    else:
        await rq.delete_items_by_name(item_name)
        await state.clear()
        await message.answer(f'Кроссовки {item_name} успешно были удалены!')
        


@router.callback_query(F.data == 'del_category')
async def del_category(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите название категории')
    await state.set_data({})
    await state.set_state(Del_Category.category_name)


@router.message(Del_Category.category_name)
async def process_delete_category(message: types.Message, state: FSMContext):
    category_name = message.text.strip()
    
    items = await rq.get_items_by_category(category_name)
    if not items:
        await message.answer(f"Категория '{category_name}' не найдена")
        await state.clear()
        return
    
    deleted_items = await rq.delete_items_by_category(category_name)
    if not deleted_items:
        await message.answer(f"Ошибка при удалении товаров категории '{category_name}'")
        await state.clear()
        return
    
    deleted_category = await rq.delete_category(category_name)
    if not deleted_category:
        await message.answer(f"Ошибка при удалении категории '{category_name}'")
        await state.clear()
        return
    
    await message.answer(
        f"Категория '{category_name}' и {len(items)} товаров успешно удалены!"
    )
    await state.clear()
    


@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    photo = FSInputFile('D:/python/Shop-Tg-Bot/app/img/logo.png')
    telegram_id = str(callback_query.message.from_user.id)
    if telegram_id == ADMIN_ID:
        keyboard = keyboard_admin
    else:
        keyboard = keyboard_menu
    await bot.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=photo,
        caption='Приветствую! Ты попал в онлайн магазин кроссовок!',
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'catalog')
async def callback_catalog(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer(
        'Выберите категорию товара:',
        reply_markup=await categories_kb()
    )
    await callback_query.answer()

@router.callback_query(F.data.startswith('category_'))
async def category(callback_query: types.CallbackQuery):
    category_id = callback_query.data.split('_')[1]
    try:
        await callback_query.message.edit_text(
            'Выберите товар из категории:',
            reply_markup=await items_kb(int(category_id))
        )
    except:
        await callback_query.message.answer(
            'Выберите товар из категории:',
            reply_markup=await items_kb(int(category_id))
        )
    await callback_query.answer('Вы выбрали категорию')

@router.callback_query(F.data.startswith('item_'))
async def item(callback_query: types.CallbackQuery):
    item_id = callback_query.data.split('_')[1]
    item_data = await rq.get_item(item_id)
    
    if item_data:
        try:
            await callback_query.message.edit_text(
                f"<b>{item_data.name}</b>\n\n"
                f"<i>{item_data.description}</i>\n\n"
                f"Цена: <b>{item_data.price} RUB</b>",
                parse_mode="HTML",
                reply_markup=await item_detail_kb(int(item_id))
            )
        except:
            await callback_query.message.answer(
                f"<b>{item_data.name}</b>\n\n"
                f"<i>{item_data.description}</i>\n\n"
                f"Цена: <b>{item_data.price} RUB</b>",
                parse_mode="HTML",
                reply_markup=await item_detail_kb(int(item_id))
            )
    await callback_query.answer('Вы выбрали товар')

@router.callback_query(F.data.startswith('back_to_items_'))
async def back_to_items(callback_query: types.CallbackQuery):
    item_id = callback_query.data.split('_')[-1]
    item_data = await rq.get_item(item_id)
    
    if item_data:
        try:
            await callback_query.message.edit_text(
                'Выберите товар из категории:',
                reply_markup=await items_kb(item_data.category)
            )
        except:
            await callback_query.message.answer(
                'Выберите товар из категории:',
                reply_markup=await items_kb(item_data.category)
            )
    await callback_query.answer()

@router.callback_query(F.data == 'back_to_cats')
async def back_to_categories(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.edit_text(
            'Выберите категорию товара:',
            reply_markup=await categories_kb()
        )
    except:
        await callback_query.message.answer(
            'Выберите категорию товара:',
            reply_markup=await categories_kb()
        )
    await callback_query.answer()