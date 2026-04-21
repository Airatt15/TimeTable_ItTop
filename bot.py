import asyncio
from datetime import datetime, time

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = ""

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

def get_next_lesson(lessons):
    now = datetime.now().time()
    current_h, current_m = divmod(int(now.hour * 60 + now.minute), 60)
    current_str = f"{current_h:02d}:{current_m:02d}"

    for time_range, lesson in lessons:
        start_time = time_range.split('-')[0]
        h, m = map(int, start_time.split(':'))
        lesson_time = time(h, m)

        if lesson_time > now:
            return time_range, lesson
    return lessons[0]

@dp.message(F.text == "")
async def welcome_on_open(message: Message):
    welcome_text = """
👋 Привет, студент Колледжа IT TOP!

⏰ /today — пары СО ВРЕМЕНЕМ
/next — БЛИЖАЙШАЯ пара по времени!
/help — помощь и поддержка

не опаздывай на пары! 🚀
"""
    await message.answer(welcome_text)

@dp.message(Command("start"))
async def start(message: Message):
    await welcome_on_open(message)

@dp.message(Command("today"))
async def today(message: Message):
    day = DAY_MAP[datetime.now().weekday()]
    lessons = SCHEDULE.get(day, [])
    if lessons:
        text = f"📚 Сегодня ({day.capitalize()}):**\n\n"
        for time_range, lesson in lessons:
            text += f"🕐 {time_range}:{lesson}\n"
        await message.answer(text, parse_mode="Markdown")
    else:
        await message.answer("Сегодня пар нет. Отдыхай! 😎")

@dp.message(Command("next"))
async def next_lesson(message: Message):
    day = DAY_MAP[datetime.now().weekday()]
    lessons = SCHEDULE.get(day, [])
    if lessons:
        time_range, lesson = get_next_lesson(lessons)
        await message.answer(f"⏰ Ближайшая:\n🕐 {time_range}: {lesson}", parse_mode="Markdown")
    else:
        await message.answer("Сегодня пар нет!")

@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = """
🆘 Помощь и поддержка

При вопросах/предложениях пишите:
@airataiai

Разработчик бота для Колледжа IT TOP 🚀
"""
    await message.answer(help_text, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

