from app.database.models import async_session
from app.database.models import User, Item, Category

from sqlalchemy import select, delete


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()



async def add_item(name: str, price: int, description: str, category: int):
    async with async_session() as session:
        new_item = Item(name=name, price=price, description=description, category=category)
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)
            
        

async def get_items_by_category(category_name: str):
    async with async_session() as session:
        category = await session.scalar(
            select(Category.id).where(Category.name == category_name)
        )
        if not category:
            return []
        
        result = await session.execute(
            select(Item).where(Item.category == category)
        )
        return result.scalars().all()

async def delete_items_by_category(category_name: str): 
    async with async_session() as session:
        category_id = await session.scalar(
            select(Category.id).where(Category.name == category_name)
        )
        if not category_id:
            return False
        
        await session.execute(
            delete(Item).where(Item.category == category_id)
        )
        await session.commit()
        return True


async def get_id_category(category_name: str):
    async with async_session() as session:
        id = await session.scalar(
            select(Category.id).where(Category.name == category_name)
        )
        return id
    
async def get_id_item(item_name: str):
    async with async_session() as session:
        id = await session.scalar(
            select(Item.id).where(Item.name == item_name)
        )
        return id

async def delete_category(category_name: str):
    async with async_session() as session:
        result = await session.execute(
            delete(Category).where(Category.name == category_name)
        )
        await session.commit()
        return result.rowcount > 0
    
async def get_items_by_name(item_name: str):
    async with async_session() as session:
        item = await session.scalar(select(Item.id).where(Item.name == item_name))
        return item
    

async def delete_items_by_name(item_name: str):
    async with async_session() as session:
        
        item_id = await session.scalar(select(Item.id).where(Item.name == item_name))
        if not item_id:
            return False
        
        await session.execute(
            delete(Item).where(Item.id == item_id)
        )
        await session.commit()
        return True
