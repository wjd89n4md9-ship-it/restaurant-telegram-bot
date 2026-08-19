import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
print("DEBUG ENV KEYS:", list(os.environ.keys()))
print("DEBUG BOT_TOKEN:", "Є" if TOKEN else "НЕМАЄ")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🍸 Меню", callback_data="menu"),
            InlineKeyboardButton("📋 Стандарти", callback_data="standards"),
        ],
        [
            InlineKeyboardButton("🪑 Схема столів", callback_data="table_scheme"),
        ],
    ]

    await update.message.reply_text(
        "Вітаю! 👋\n\nОберіть потрібний розділ:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        keyboard = [
            [InlineKeyboardButton("🍸 Коктейлі", callback_data="cocktails")],
            [InlineKeyboardButton("🍽 Кухня", callback_data="kitchen")],
            [InlineKeyboardButton("🍺 Бар", callback_data="bar")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
        ]

        await query.edit_message_text(
            "🍽 Оберіть меню:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "standards":
        keyboard = [
            [InlineKeyboardButton("📋 Чек-лист", callback_data="checklist")],
            [InlineKeyboardButton("🗣 Скрипт офіціанта", callback_data="waiter_script")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
        ]

        await query.edit_message_text(
            "📋 Оберіть стандарт:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "back":
        await show_main_menu(query)

    elif query.data in [
        "cocktails",
        "kitchen",
        "bar",
        "checklist",
        "waiter_script",
        "table_layout",
        "table_scheme",
    ]:

        files = {
            "cocktails": "files/menu/cocktails.pdf",
            "kitchen": "files/menu/kitchen.pdf",
            "bar": "files/menu/bar.pdf",
            "checklist": "files/standards/checklist.pdf",
            "waiter_script": "files/standards/waiter_script.pdf",
            "table_layout": "files/standards/table_layout.pdf",
            "table_scheme": "files/tables/table_scheme.pdf",
        }

        file_path = files[query.data]

        if not os.path.exists(file_path):
            await query.message.reply_text("❌ Файл не знайдено.")
            return

        if os.path.getsize(file_path) == 0:
            await query.message.reply_text("❌ Файл порожній.")
            return

        await query.message.reply_document(document=file_path)


async def show_main_menu(query):
    keyboard = [
        [
            InlineKeyboardButton("🍸 Меню", callback_data="menu"),
            InlineKeyboardButton("📋 Стандарти", callback_data="standards"),
        ],
        [
            InlineKeyboardButton("🪑 Схема столів", callback_data="table_scheme"),
        ],
    ]

    await query.edit_message_text(
        "Вітаю! 👋\n\nОберіть потрібний розділ:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def main():
    if not TOKEN:
        raise ValueError("Не знайдено BOT_TOKEN.")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущений...")

    application.run_polling()


if __name__ == "__main__":
    main()
