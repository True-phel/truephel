from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import os
from rapidfuzz import process, fuzz
from dotenv import load_dotenv  # ← додано

load_dotenv()  # ← завантажує .env файл

TOKEN = os.getenv("BOT_TOKEN", "token")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ─── База рецептів ────────────────────────────────────────────────
recipes = {
    # Сніданки
    "оладки": {
        "emoji": "🥞",
        "category": "🌅 Сніданок",
        "time": "20 хв",
        "text": (
            "🥞 *Оладки*\n\n"
            "📋 *Інгредієнти:*\n"
            "• 250 мл кефіру\n"
            "• 1 яйце\n"
            "• 1 ст.л. цукру\n"
            "• 1 ч.л. соди\n"
            "• ~1 склянка борошна\n"
            "• щіпка солі\n\n"
            "👨‍🍳 *Приготування:*\n"
            "1. Змішати кефір, яйце, цукор, сіль.\n"
            "2. Додати соду та борошно, перемішати до однорідності.\n"
            "3. Смажити на олії до золотої скоринки з обох сторін.\n\n"
            "⏱ Час: 20 хв | 🍽 Порцій: 4"
        ),
    },
    "омлет": {
        "emoji": "🍳",
        "category": "🌅 Сніданок",
        "time": "10 хв",
        "text": (
            "🍳 *Омлет*\n\n"
            "📋 *Інгредієнти:*\n"
            "• 3 яйця\n"
            "• 50 мл молока\n"
            "• сіль, перець\n"
            "• вершкове масло\n\n"
            "👨‍🍳 *Приготування:*\n"
            "1. Збити яйця з молоком, сіллю та перцем.\n"
            "2. Розтопити масло на пательні.\n"
            "3. Вилити яєчну суміш, готувати під кришкою 5–7 хв.\n\n"
            "⏱ Час: 10 хв | 🍽 Порцій: 1"
        ),
    },
    "вівсянка": {
        "emoji": "🥣",
        "category": "🌅 Сніданок",
        "time": "10 хв",
        "text": (
            "🥣 *Вівсянка*\n\n"
            "📋 *Інгредієнти:*\n"
            "• 100 г вівсяних пластівців\n"
            "• 250 мл молока\n"
            "• 1 ст.л. меду\n"
            "• фрукти за смаком\n\n"
            "👨‍🍳 *Приготування:*\n"
            "1. Закипятити молоко.\n"
            "2. Додати пластівці, варити 5 хв.\n"
            "3. Додати мед та нарізані фрукти.\n\n"
            "⏱ Час: 10 хв | 🍽 Порцій: 1"
        ),
    },
    # Обіди / основні страви
    "борщ": {
        "emoji": "🍲",
        "category": "🥘 Суп",
        "time": "90 хв",
        "text": (
            "🍲 *Борщ*\n\n"
            "📋 *Інгредієнти:*\n"
            "• 500 г яловичини\n"
            "• 1 буряк\n"
            "• 200 г капусти\n"
            "• 2 картоплини\n"
            "• 1 морква, 1 цибуля\n"
            "• 2 ст.л. томатної пасти\n"
            "• лавровий лист, сіль\n\n"
            "👨‍🍳 *Приготування:*\n"
            "1. Зварити бульйон із яловичини (60 хв).\n"
            "2. Обсмажити цибулю, моркву, буряк з томатом.\n"
            "3. Додати картоплю, потім капусту та зажарку.\n"
            "4. Варити ще 20 хв, посолити.\n\n"
            "⏱ Час: 90 хв | 🍽 Порцій: 6"
        ),
    },
    "паста карбонара": {
        "emoji": "🍝",
        "category": "🍽 Основна страва",
        "time": "25 хв",
        "text": (
            "🍝 *Паста Карбонара*\n\n"
            "📋 *Інгредієнти:*\n"
            "• 200 г спагеті\n"
            "• 100 г бекону/панчетти\n"
            "• 2 яйця + 1 жовток\n"
            "• 50 г пармезану\n"
            "• чорний перець, сіль\n\n"
            "👨‍🍳 *Приготування:*\n"
            "1. Зварити спагеті al dente.\n"
            "2. Обсмажити бекон до хрусткості.\n"
            "3. Змішати яйця з тертим пармезаном та перцем.\n"
            "4. Зняти пасту з вогню, додати яєчну суміш і бекон. Перемішати — яйця мають загустіти від тепла, але не згорнутись.\n\n"
            "⏱ Час: 25 хв | 🍽 Порцій: 2"
        ),
    },
    "курка в духовці": {
        "emoji": "🍗",
        "category": "🍽 Основна страва",
        "time": "60 хв",
        "text": (
            "🍗 *Курка в духовці*\n\n"
            "📋 *Інгредієнти:*\n"
            "• 1 кг курячих стегон\n"
            "• 3 зубчики часнику\n"
            "• 2 ст.л. олії\n"
            "• паприка, сіль, перець, розмарин\n\n"
            "👨‍🍳 *Приготування:*\n"
            "1. Натерти курку сумішшю олії, часнику та спецій.\n"
            "2. Залишити маринуватись 30 хв.\n"
            "3. Запікати при 200°C протягом 40–45 хв.\n\n"
            "⏱ Час: 60 хв | 🍽 Порцій: 4"
        ),
    },
    # Десерти
    "шоколадний кекс": {
        "emoji": "🍰",
        "category": "🍮 Десерт",
        "time": "45 хв",
        "text": (
            "🍰 *Шоколадний кекс*\n\n"
            "📋 *Інгредієнти:*\n"
            "• 200 г борошна\n"
            "• 150 г цукру\n"
            "• 3 яйця\n"
            "• 100 г масла\n"
            "• 50 г какао\n"
            "• 1 ч.л. розпушувача\n\n"
            "👨‍🍳 *Приготування:*\n"
            "1. Збити масло з цукром, додати яйця.\n"
            "2. Просіяти борошно, какао та розпушувач — додати до маси.\n"
            "3. Вилити в форму, запікати при 180°C — 35 хв.\n\n"
            "⏱ Час: 45 хв | 🍽 Порцій: 8"
        ),
    },
    "сирники": {
        "emoji": "🧀",
        "category": "🍮 Десерт",
        "time": "30 хв",
        "text": (
            "🧀 *Сирники*\n\n"
            "📋 *Інгредієнти:*\n"
            "• 500 г сиру (5–9%)\n"
            "• 2 яйця\n"
            "• 3 ст.л. цукру\n"
            "• 5 ст.л. борошна\n"
            "• ванілін, щіпка солі\n\n"
            "👨‍🍳 *Приготування:*\n"
            "1. Змішати сир, яйця, цукор, сіль, ванілін.\n"
            "2. Додати борошно, замісити тісто.\n"
            "3. Сформувати коржики, обваляти в борошні.\n"
            "4. Смажити на олії до золотавої скоринки.\n\n"
            "⏱ Час: 30 хв | 🍽 Порцій: 3"
        ),
    },
}

# Категорії для меню
CATEGORIES = {
    "🌅 Сніданок": ["оладки", "омлет", "вівсянка"],
    "🥘 Суп": ["борщ"],
    "🍽 Основна страва": ["паста карбонара", "курка в духовці"],
    "🍮 Десерт": ["шоколадний кекс", "сирники"],
}

FUZZY_THRESHOLD = 65  # мінімальна схожість для нечіткого пошуку


# ─── Клавіатури ───────────────────────────────────────────────────

def main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📖 Всі рецепти", callback_data="menu_all")],
        [InlineKeyboardButton(text="🎲 Випадковий рецепт", callback_data="random")],
    ]
    for cat in CATEGORIES:
        buttons.append([InlineKeyboardButton(text=cat, callback_data=f"cat_{cat}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def category_keyboard(category: str) -> InlineKeyboardMarkup:
    buttons = []
    for name in CATEGORIES[category]:
        r = recipes[name]
        buttons.append([
            InlineKeyboardButton(
                text=f"{r['emoji']} {name.capitalize()} ({r['time']})",
                callback_data=f"recipe_{name}",
            )
        ])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def recipe_keyboard(recipe_name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ До меню", callback_data="back_main")],
        [InlineKeyboardButton(text="🎲 Інший рецепт", callback_data="random")],
    ])


def suggestions_keyboard(matches: list[str]) -> InlineKeyboardMarkup:
    buttons = []
    for name in matches:
        r = recipes[name]
        buttons.append([
            InlineKeyboardButton(
                text=f"{r['emoji']} {name.capitalize()}",
                callback_data=f"recipe_{name}",
            )
        ])
    buttons.append([InlineKeyboardButton(text="📖 Всі рецепти", callback_data="menu_all")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ─── Хендлери команд ──────────────────────────────────────────────

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Вітаю! Я *Рецепт-бот*.\n\n"
        "Напишіть назву страви — знайду рецепт навіть якщо є помилки у слові.\n"
        "Або скористайтеся меню нижче 👇",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer(
        "📋 *Головне меню*",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    import random
    name = random.choice(list(recipes.keys()))
    r = recipes[name]
    await message.answer(
        r["text"],
        parse_mode="Markdown",
        reply_markup=recipe_keyboard(name),
    )


# ─── Нечіткий пошук ───────────────────────────────────────────────

def fuzzy_search(query: str) -> list[str]:
    """Повертає список назв рецептів, що найбільше схожі на запит."""
    all_names = list(recipes.keys())

    # Спочатку точний збіг
    if query in all_names:
        return [query]

    # Нечіткий пошук (scorer=WRatio враховує підрядки + транспозиції)
    results = process.extract(
        query,
        all_names,
        scorer=fuzz.WRatio,
        limit=3,
    )
    matched = [name for name, score, _ in results if score >= FUZZY_THRESHOLD]
    return matched


@dp.message()
async def handle_text(message: types.Message):
    query = message.text.lower().strip()
    matches = fuzzy_search(query)

    if not matches:
        await message.answer(
            "😕 Не знайшов такого рецепта.\n"
            "Спробуй написати інакше або обери зі списку:",
            reply_markup=main_menu_keyboard(),
        )
        return

    if len(matches) == 1:
        r = recipes[matches[0]]
        await message.answer(
            r["text"],
            parse_mode="Markdown",
            reply_markup=recipe_keyboard(matches[0]),
        )
    else:
        names_str = ", ".join(f"*{n}*" for n in matches)
        await message.answer(
            f"🔍 Знайшов кілька варіантів для *«{message.text}»*:\n{names_str}\n\nОбери один:",
            parse_mode="Markdown",
            reply_markup=suggestions_keyboard(matches),
        )


# ─── Callback-хендлери (кнопки) ───────────────────────────────────

@dp.callback_query(F.data == "back_main")
async def cb_back_main(call: types.CallbackQuery):
    await call.message.edit_text(
        "📋 *Головне меню*",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )
    await call.answer()


@dp.callback_query(F.data == "menu_all")
async def cb_menu_all(call: types.CallbackQuery):
    lines = []
    for cat, names in CATEGORIES.items():
        lines.append(f"\n{cat}")
        for n in names:
            r = recipes[n]
            lines.append(f"  {r['emoji']} {n.capitalize()} — {r['time']}")
    await call.message.edit_text(
        "📖 *Всі рецепти:*" + "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )
    await call.answer()


@dp.callback_query(F.data == "random")
async def cb_random(call: types.CallbackQuery):
    import random
    name = random.choice(list(recipes.keys()))
    r = recipes[name]
    await call.message.edit_text(
        r["text"],
        parse_mode="Markdown",
        reply_markup=recipe_keyboard(name),
    )
    await call.answer()


@dp.callback_query(F.data.startswith("cat_"))
async def cb_category(call: types.CallbackQuery):
    category = call.data[4:]  # прибрати префікс "cat_"
    if category not in CATEGORIES:
        await call.answer("Категорія не знайдена.")
        return
    await call.message.edit_text(
        f"*{category}*\n\nОбери рецепт:",
        parse_mode="Markdown",
        reply_markup=category_keyboard(category),
    )
    await call.answer()


@dp.callback_query(F.data.startswith("recipe_"))
async def cb_recipe(call: types.CallbackQuery):
    name = call.data[7:]  # прибрати префікс "recipe_"
    if name not in recipes:
        await call.answer("Рецепт не знайдений.")
        return
    r = recipes[name]
    await call.message.edit_text(
        r["text"],
        parse_mode="Markdown",
        reply_markup=recipe_keyboard(name),
    )
    await call.answer()


# ─── Запуск ───────────────────────────────────────────────────────

async def main():
    print("🤖 Бот запущено!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())