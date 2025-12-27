import asyncio
import random
import copy
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from openpyxl import load_workbook

BOT_TOKEN = "8463283642:AAGze2iC9GAgqUxcDrTUoaKBclBnUhmBrDw"
XLSX_PATH = "fic.xlsx"


# ---------- FSM ----------

class QuizState(StatesGroup):
    choosing_topic = State()
    answering = State()


# ---------- Загрузка Excel ----------

def load_quiz_from_xlsx(path: str) -> dict:
    wb = load_workbook(path)
    data = {}

    for sheet in wb.sheetnames:
        ws = wb[sheet]
        questions = []

        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or not row[0]:
                continue

            question = str(row[0]).strip()

            options = [
                str(row[1]).strip(),
                str(row[2]).strip(),
                str(row[3]).strip(),
                str(row[4]).strip()
            ]

            correct = str(row[5]).strip()

            questions.append({
                "question": question,
                "options": options,
                "correct": correct
            })

        data[sheet] = questions

    return data



QUIZ_DATA = load_quiz_from_xlsx(XLSX_PATH)


# ---------- Клавиатуры ----------

def topics_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=topic, callback_data=f"topic:{topic}")]
            for topic in QUIZ_DATA.keys()
        ]
    )


def answers_keyboard(options):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=opt, callback_data=f"answer:{opt}")]
            for opt in options
        ]
    )


def next_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Далее", callback_data="next"),
                InlineKeyboardButton(text="Закончить", callback_data="finish")
            ],
            [InlineKeyboardButton(text="Другая тема", callback_data="change_topic")]
        ]
    )


# ---------- Бот ----------

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(QuizState.choosing_topic)

    await message.answer(
        "Выберите тему",
        reply_markup=topics_keyboard()
    )


@dp.callback_query(F.data.startswith("topic:"))
async def choose_topic(call: CallbackQuery, state: FSMContext):
    topic = call.data.split(":", 1)[1]

    questions = copy.deepcopy(QUIZ_DATA[topic])
    random.shuffle(questions)

    await state.update_data(
        topic=topic,
        questions=questions,
        index=0
    )

    await state.set_state(QuizState.answering)

    await call.message.edit_text(f"Тема выбрана: **{topic}**")
    await send_question(call.message, state)


async def send_question(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    questions = data["questions"]

    if index >= len(questions):
        await message.answer("Вопросы закончились")
        await state.clear()
        return

    q = questions[index]

    await message.answer(
        f"{q['question']}",
        reply_markup=answers_keyboard(q["options"])
    )



@dp.callback_query(F.data.startswith("answer:"))
async def answer_question(call: CallbackQuery, state: FSMContext):
    user_answer = call.data.split(":", 1)[1]
    data = await state.get_data()

    index = data["index"]
    question = data["questions"][index]

    correct = question["correct"]

    if user_answer == correct:
        text = "Верно"
    else:
        text = f"Неверно.\nПравильный ответ: {correct}"

    await call.message.edit_text(text, reply_markup=next_keyboard())



@dp.callback_query(F.data == "next")
async def next_question(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(index=data["index"] + 1)
    await send_question(call.message, state)


@dp.callback_query(F.data == "finish")
async def finish_quiz(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Прохождение завершено. Начать заново /start")


@dp.callback_query(F.data == "change_topic")
async def change_topic(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(QuizState.choosing_topic)
    await call.message.edit_text("Выберите тему", reply_markup=topics_keyboard())


# ---------- Запуск ----------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

