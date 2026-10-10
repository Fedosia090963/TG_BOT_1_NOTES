"""Обработчики команд и сообщений Telegram-бота."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, Message

from app.database import Database
from app.keyboards import get_main_keyboard

router = Router()


class AddTaskState(StatesGroup):
    waiting_for_task_text = State()


def get_database() -> Database:
    """Создаёт объект базы данных."""
    return Database("tasks.db")


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    """Приветствует пользователя и показывает доступные команды."""
    await message.answer(
        "Привет! Я бот для командной работы.\n"
        "Используйте /add, /list или /list_csv.",
        reply_markup=get_main_keyboard(),
    )


@router.message(Command("add"))
async def command_add(message: Message, state: FSMContext) -> None:
    """Начинает добавление задачи или сохраняет её, если текст передан в команде."""
    text = message.text or ""
    task_text = text.replace("/add", "", 1).strip()

    if task_text:
        await save_task(message, task_text)
        return

    await message.answer("Отправьте текст задачи. Я сохраню её в общий список.")
    await state.set_state(AddTaskState.waiting_for_task_text)


@router.message(AddTaskState.waiting_for_task_text)
async def add_task_from_message(message: Message, state: FSMContext) -> None:
    """Сохраняет задачу, полученную следующим сообщением."""
    await save_task(message, message.text or "")
    await state.clear()


async def save_task(message: Message, task_text: str) -> None:
    """Сохраняет задачу и сообщает пользователю результат."""
    database = get_database()
    try:
        task_id = database.add_task(task_text, str(message.from_user.id))
    except ValueError:
        await message.answer("Текст задачи не может быть пустым.")
        return
    finally:
        database.close()

    await message.answer(
        f"Задача сохранена!\n"
        f"Номер: {task_id}\n"
        f"Текст: {task_text}"
    )


@router.message(Command("list"))
async def command_list(message: Message) -> None:
    """Показывает все задачи текстом."""
    database = get_database()
    tasks = database.get_all_tasks()
    database.close()

    if not tasks:
        await message.answer("Список задач пуст.")
        return

    lines = ["Все задачи:"]
    for task in tasks:
        lines.append(
            f"{task['id']}. {task['text']} "
            f"(пользователь: {task['user']}, "
            f"создано: {task['created_at']})"
        )

    await message.answer("\n".join(lines))


@router.message(Command("list_csv"))
async def command_list_csv(message: Message) -> None:
    """Отправляет все задачи в формате CSV."""
    database = get_database()
    csv_text = database.export_tasks_to_csv()
    database.close()

    file = BufferedInputFile(
        file=csv_text.encode("utf-8"),
        filename="tasks.csv",
    )
    await message.answer_document(file)
