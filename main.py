import asyncio
import json
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

TOKEN = "8838600669:AAFOrN7m1Rpi3cwG_BUrNOwSrWLwiuiUZW0"

with open("data.json", "r", encoding="utf-8") as f:
    portfolio_data = json.load(f)

dp = Dispatcher()

def get_main_menu():
    kb = [
        [
            KeyboardButton(text=portfolio_data["about"]["title"]),
            KeyboardButton(text=portfolio_data["goal"]["title"]),
        ],
        [
            KeyboardButton(text=portfolio_data["history"]["title"]),
            KeyboardButton(text=portfolio_data["mentor"]["title"]),
        ],
        [
            KeyboardButton(text=portfolio_data["progress"]["title"]),
            KeyboardButton(text=portfolio_data["hobbies"]["title"]),
        ],
        [
            KeyboardButton(text=portfolio_data["projects"]["title"]),
            KeyboardButton(text=portfolio_data["github"]["title"]),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}! "
        f"Добро пожаловать в бот-портфолио Ергазина Рахата. "
        f"Используй меню ниже, чтобы узнать обо мне больше!",
        reply_markup=get_main_menu(),
    )

@dp.message(lambda msg: msg.text == portfolio_data["about"]["title"])
async def show_about(message: Message):
    info = portfolio_data["about"]
    facts = "\n".join([f"• {fact}" for fact in info["facts"]])
    text = (
        f"📌 {html.bold(info['title'])}\n\n"
        f"👤 {html.bold('Имя:')} {info['name']}\n"
        f"🎂 {html.bold('Возраст:')} {info['age']} лет\n"
        f"💼 {html.bold('Занятие:')} {info['occupation']}\n\n"
        f"{html.italic('Факты:')}\n{facts}"
    )
    await message.answer(text)


@dp.message(lambda msg: msg.text == portfolio_data["goal"]["title"])
async def show_goal(message: Message):
    info = portfolio_data["goal"]
    text = f"🎯 {html.bold(info['title'])}\n\n{info['text']}"
    await message.answer(text)


@dp.message(lambda msg: msg.text == portfolio_data["history"]["title"])
async def show_history(message: Message):
    info = portfolio_data["history"]
    text = f"🚀 {html.bold(info['title'])}\n\n{info['text']}"
    await message.answer(text)


@dp.message(lambda msg: msg.text == portfolio_data["mentor"]["title"])
async def show_mentor(message: Message):
    info = portfolio_data["mentor"]
    text = f"🤝 {html.bold(info['title'])}\n\n{info['text']}"
    await message.answer(text)

@dp.message(lambda msg: msg.text == portfolio_data["progress"]["title"])
async def show_progress(message: Message):
    info = portfolio_data["progress"]
    text = f"📈 {html.bold(info['title'])}\n\n{info['text']}"
    await message.answer(text)


@dp.message(lambda msg: msg.text == portfolio_data["hobbies"]["title"])
async def show_hobbies(message: Message):
    info = portfolio_data["hobbies"]
    text = f"🎮 {html.bold(info['title'])}\n\n{info['text']}"
    await message.answer(text)


@dp.message(lambda msg: msg.text == portfolio_data["projects"]["title"])
async def show_projects(message: Message):
    info = portfolio_data["projects"]
    await message.answer(f"💻 {html.bold(info['title'])}:")

    for item in info["items"]:
        text = f"🔹 {html.bold(item['name'])}\n📝 {item['desc']}"

        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Открыть проект", url=item["link"])]
            ]
        )
        await message.answer(text, reply_markup=inline_kb)


@dp.message(lambda msg: msg.text == portfolio_data["github"]["title"])
async def show_github(message: Message):
    info = portfolio_data["github"]

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Перейти на GitHub", url=info["url"])]
        ]
    )
    await message.answer(f"📂 {info['title']}", reply_markup=inline_kb)

async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())