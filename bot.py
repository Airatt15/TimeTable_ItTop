import asyncio
from datetime import datetime, time

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8507173948:AAGlCQqzBY8n3AdSLKY5kAbrEhDNFlAgmVo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

SCHEDULE = {
    "понедельник": [
        ("10:10-11:40", "Математика"),
        ("12:30-14:00", "Русский язык"),
        ("14:10-15:40", "Информатика"),
        ("15:50-17:20", "Физическая культура")
    ],
    "вторник": [
        ("08:30-10:00", "Литература"),
        ("10:10-11:40", "География"),
        ("12:30-14:00", "Конфигурирование Windows 10"),
        ("14:10-15:40", "Иностранный язык"),
        ("15:50-17:20", "Физическая культура")
    ],
    "среда": [
        ("08:30-10:00", "Физика"),
        ("10:10-11:40", "Информатика"),
        ("12:30-14:00", "Интернет-Маркетинг"),
        ("14:10-15:40", "Математика")
    ],
    "четверг": [
        ("14:10-15:40", "Индивидуальный проект"),
        ("15:50-17:20", "Интернет-Маркетинг")
    ],
    "пятница": [
        ("12:30-14:00", "Химия"),
        ("14:10-15:40", "ОБЗР")
    ],
    "суббота": [],
    "воскресенье": []
}

DAY_MAP = {
    0: "понедельник", 1: "вторник", 2: "среда", 3: "четверг",
    4: "пятница", 5: "суббота", 6: "воскресенье",
}

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📚 Сегодня", callback_data="today")
    builder.button(text="⏰ Следующая пара", callback_data="next")
    builder.button(text="🆘 Помощь", callback_data="help")
    builder.button(text="💬 Поддержка", callback_data="support")
    builder.button(text="📅 Все дни недели", callback_data="all_days")
    builder.adjust(2)
    return builder

def get_day_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📌 Понедельник", callback_data="day_понедельник")
    builder.button(text="📌 Вторник", callback_data="day_вторник")
    builder.button(text="📌 Среда", callback_data="day_среда")
    builder.button(text="📌 Четверг", callback_data="day_четверг")
    builder.button(text="📌 Пятница", callback_data="day_пятница")
    builder.button(text="📌 Суббота", callback_data="day_суббота")
    builder.button(text="📌 Воскресенье", callback_data="day_воскресенье")
    builder.button(text="⬅️ Назад", callback_data="back")
    builder.adjust(2)
    return builder

def get_support_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Написать @airataiai", url="https://t.me/airataiai")
    builder.button(text="⬅️ Назад", callback_data="back")
    builder.adjust(1)
    return builder

def get_next_lesson(lessons):
    now = datetime.now().time()

    for time_range, lesson in lessons:
        start_time = time_range.split('-')[0]
        h, m = map(int, start_time.split(':'))
        lesson_time = time(h, m)

        if lesson_time > now:
            return time_range, lesson

    return lessons[0]

@dp.message(Command("start"))
async def start(message: Message):
    welcome_text = """
👋 Привет, студент Колледжа IT TOP!

⏰ Покажи своё расписание:
📚 Сегодня — пары СО ВРЕМЕНЕМ
⏰ Следующая пара — БЛИЖАЙШАЯ пара по времени!
📅 Все дни недели — полное расписание
🆘 Помощь — помощь и поддержка
💬 Поддержка — написать разработчику

Не опаздывай на пары! 🚀
"""
    await message.answer(welcome_text, reply_markup=get_main_keyboard().as_markup())

@dp.message(Command("today"))
async def today(message: Message):
    day = DAY_MAP[datetime.now().weekday()]
    lessons = SCHEDULE.get(day, [])
    if lessons:
        text = f"📚 Сегодня ({day.capitalize()}):\n\n"
        for time_range, lesson in lessons:
            text += f"🕐 {time_range}: {lesson}\n"
        await message.answer(text, reply_markup=get_main_keyboard().as_markup())
    else:
        await message.answer("Сегодня пар нет. Отдыхай! 😎", reply_markup=get_main_keyboard().as_markup())

@dp.message(Command("next"))
async def next_lesson(message: Message):
    day = DAY_MAP[datetime.now().weekday()]
    lessons = SCHEDULE.get(day, [])
    if lessons:
        time_range, lesson = get_next_lesson(lessons)
        await message.answer(
            f"⏰ Ближайшая:\n🕐 {time_range}: {lesson}",
            reply_markup=get_main_keyboard().as_markup()
        )
    else:
        await message.answer("Сегодня пар нет!", reply_markup=get_main_keyboard().as_markup())

@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = """
🆘 Помощь и поддержка

При вопросах/предложениях пишите:
@airataiai

Разработчик бота для Колледжа IT TOP 🚀
"""
    await message.answer(help_text, reply_markup=get_main_keyboard().as_markup())

@dp.message(Command("all_days"))
async def all_days(message: Message):
    text = "📅 Выберите день недели:\n"
    await message.answer(text, reply_markup=get_day_keyboard().as_markup())

@dp.message(Command("support"))
async def support_command(message: Message):
    support_text = """
💬 Поддержка и связь с разработчиком

При вопросах/предложениях пишите напрямую:
@airataiai

Разработчик бота для Колледжа IT TOP 🚀
"""
    await message.answer(support_text, reply_markup=get_support_keyboard().as_markup())

@dp.callback_query(F.data == "today")
async def cb_today(callback: CallbackQuery):
    await today(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "next")
async def cb_next(callback: CallbackQuery):
    await next_lesson(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery):
    await help_command(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "support")
async def cb_support(callback: CallbackQuery):
    await support_command(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "all_days")
async def cb_all_days(callback: CallbackQuery):
    await all_days(callback.message)
    await callback.answer()

@dp.callback_query(F.data.startswith("day_"))
async def cb_day(callback: CallbackQuery):
    day = callback.data.split("day_")[1]
    lessons = SCHEDULE.get(day, [])
    if lessons:
        text = f"📅 {day.capitalize()}:\n\n"
        for time_range, lesson in lessons:
            text += f"🕐 {time_range}: {lesson}\n"
        await callback.message.answer(text, reply_markup=get_day_keyboard().as_markup())
    else:
        await callback.message.answer(f"📅 {day.capitalize()}: пар нет. Отдыхай! 😎", reply_markup=get_day_keyboard().as_markup())
    await callback.answer()

@dp.callback_query(F.data == "back")
async def cb_back(callback: CallbackQuery):
    welcome_text = """
👋 Привет, студент Колледжа IT TOP!

⏰ Покажи своё расписание:
📚 Сегодня — пары СО ВРЕМЕНЕМ
⏰ Следующая пара — БЛИЖАЙШАЯ пара по времени!
📅 Все дни недели — полное расписание
🆘 Помощь — помощь и поддержка
💬 Поддержка — написать разработчику

Не опаздывай на пары! 🚀
"""
    await callback.message.answer(welcome_text, reply_markup=get_main_keyboard().as_markup())
    await callback.answer()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
