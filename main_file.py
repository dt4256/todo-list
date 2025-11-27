from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram import *
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

    
    





bot = Bot(token=TOKEN)
dp = Dispatcher()


with open("data/timezones.json", "r", encoding="utf-8") as f:
    TIMEZONES = json.load(f)



class SettingsStates(StatesGroup):
    editing_timezone = State()
    editing_time_call = State()




@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    t=add_user(user_id)
    print(t)
    await message.answer(t)
    

@dp.message(Command("settings"))
async def settings_handler(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Часовой пояс")],
            [KeyboardButton(text="За сколько уведомить до окончания дедлайна")],
            [KeyboardButton(text="Способ вывода задач")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True  
    )
    await message.answer("Что изменить?", reply_markup=kb)



@dp.message(F.text == "Часовой пояс")
async def tz_start(message: Message, state: FSMContext):
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"tz:{name}")] for name in TIMEZONES]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберите часовой пояс:", reply_markup=kb)
    await state.set_state(SettingsStates.editing_timezone)


@dp.callback_query(F.data.startswith("tz:"), SettingsStates.editing_timezone)
async def tz_save(callback: CallbackQuery, state: FSMContext):
    user_id = str(callback.from_user.id)
    name = callback.data[3:]
    if name in TIMEZONES:
        with open(f"user_data/{user_id}/preferences", "r", encoding="utf-8") as f:
            p = json.load(f)
        p["utc_loc"] = TIMEZONES[name]
        with open(f"user_data/{user_id}/preferences", "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=2)
        await callback.message.edit_text("Часовой пояс сохранён.")
    await state.clear()
    await callback.answer()



@dp.message(F.text == "За сколько уведомить до окончания дедлайна")
async def time_call_start(message: Message, state: FSMContext):
    await message.answer("Введите время звонка в формате ЧЧ:ММ (например, 09:30):")
    await state.set_state(SettingsStates.editing_time_call)


@dp.message(SettingsStates.editing_time_call)
async def time_call_save(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    try:
        datetime.datetime.strptime(message.text.strip(), "%H:%M")
        with open(f"user_data/{user_id}/preferences", "r", encoding="utf-8") as f:
            p = json.load(f)
        p["time_call"] = message.text.strip()
        with open(f"user_data/{user_id}/preferences", "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=2)
        await message.answer("Время звонка сохранено.")
    except:
        await message.answer("Неверный формат. Введите ЧЧ:ММ (например, 14:00).")
        return
    await state.clear()



@dp.message(F.text == "Способ вывода задач")
async def way_start(message: Message):
    buttons = [
        [InlineKeyboardButton(text="Text", callback_data="way:text")],
        [InlineKeyboardButton(text="Using photos", callback_data="way:graphix")]
        
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберите способ уведомлений:", reply_markup=kb)


@dp.callback_query(F.data.startswith("way:"))
async def way_save(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    method = callback.data[4:] 

    if method not in ("text","graphix"):
        await callback.answer("Недопустимый вариант.", show_alert=True)
        return

    try:
        with open(f"user_data/{user_id}/preferences", "r", encoding="utf-8") as f:
            prefs = json.load(f)
        prefs["waytoinfo"] = method
        with open(f"user_data/{user_id}/preferences", "w", encoding="utf-8") as f:
            json.dump(prefs, f, ensure_ascii=False, indent=2)
        await callback.message.edit_text(f"Способ уведомлений: {method}")
    except:
        await callback.message.edit_text("Ошибка сохранения.")
    await callback.answer()


# === Назад ===
@dp.message(F.text == "⬅️ Назад")
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Меню настроек закрыто.")




async def main():
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())