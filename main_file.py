from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode4
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.types import CallbackQuery
import asyncio

import json
import datetime
import os
TOKEN = "not now"

def add_user(user_id):
    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        if user_id not in data:
            data.append(user_id) 
            os.mkdir(f"user_data/{user_id}")
            with open(f"user_data/{user_id}/preferences","w",encoding="utf-8") as f:
                #ТУТ ДОРАБАТЫВАТЬ ПРЕДПОЧТЕНИЯ ПРИ ИНИЦИАЛИЗАЦИИ
                tmp_preference={"permittions":"user","utc_loc":"","time_call":"","waytoinfo":""}
                json.dump(tmp_preference,f,ensure_ascii=False,indent=2)
            with open(f"user_data/{user_id}/problems","w",encoding="utf-8") as f:
                problems=[]
            with open("data/users.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return "initialised"
        else:
            return "already in"   
    except:
        return "smth gone wrong"       

    
    


def settings(used_id):
    return



bot = Bot(token=TOKEN)
dp = Dispatcher()

# Состояния FSM для редактирования настроек
class SettingsStates(StatesGroup):
    editing_timezone = State()
    editing_language = State()




@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    t=add_user(user_id)
    print(t)
    await message.answer(t)
    





async def main():
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())