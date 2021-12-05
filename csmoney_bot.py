import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data
import os
import time

bot = Bot(token=os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['🔪 Ножи', '🥊 Перчатки', '🔫 Снайперские винтовки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Выберите категорию', reply_markup=keyboard)
    

@dp.message_handler(Text(equals='🔪 Ножи'))
async def get_discount_knives(message: types.Message):
    await get_discount(cat_type=2)
        
        
@dp.message_handler(Text(equals='🔫 Снайперские винтовки'))
async def get_discount_guns(message: types.Message):
    await get_discount(cat_type=4)

    
async def get_discount(cat_type=2):
    await message.answer('Please waiting...')
    
    collect_data(cat_type=cat_type)
    
    with open('result.json') as file:
        data = json.load(file)
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
            f'{hbold("Цена: ")}${item.get("item_price")}🔥'
    
        if index%20 == 0:
            time.sleep(3)
            
        await message.answer(card)    
    
def main():
    executor.start_polling(dp)
    
    
if __name__ == '__main__':
    main()
    
