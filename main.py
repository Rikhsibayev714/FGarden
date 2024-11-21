import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import InputFile, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Полный путь к вашему .env файлу
dotenv_path = "./TELEGRAM_TOKEN.env"

# Проверяем наличие файла .env
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f"Файл {dotenv_path} не найден. Проверьте путь.")

# Загружаем переменные из .env
load_dotenv(dotenv_path)

# Токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Проверяем, что токен загрузился
if not TOKEN:
    raise ValueError("Токен Telegram не найден! Проверьте переменную TELEGRAM_TOKEN в файле .env.")

print(f"Токен успешно загружен: {TOKEN}")

# Логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Список разрешенных ID
ALLOWED_IDS = [1164878660, 117441349, 7168656057, 51804137]

# Функция, которая будет обрабатывать команду /start
async def start(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ALLOWED_IDS:
        await update.message.reply_text(
            "Извините, у вас нет доступа к этому боту. Свяжитесь с Рихсибаевом Отабеком! @Rikhsibayev714"
        )
        return

    keyboard = [["План-Факт"], ["Поступление"], ["Дебеторка"], ["Продажа-кунлик"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Выберите нужный раздел:", reply_markup=reply_markup)

# Функция, которая будет обрабатывать команду /get_id
async def get_id(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Ваш ID: {user_id}")

# Функция для обработки сообщений с кнопок
async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_IDS:
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
        return

    current_date = datetime.now().strftime("%Y-%m-%d")
    text = update.message.text
    file_map = {
        "План-Факт": "План-факт.png",
        "Поступление": "Поступление.png",
        "Дебеторка": "Дебеторка.png",
        "Продажа-кунлик": "Продажа-кунлик.png"
    }

    if text in file_map:
        file_name = file_map[text]
        try:
            with open(file_name, 'rb') as photo_file:
                photo = InputFile(photo_file)
                await update.message.reply_text(f"Вы выбрали {text}. Дата обновления: {current_date}")
                await update.message.reply_document(document=photo)
        except FileNotFoundError:
            await update.message.reply_text(f"Файл '{file_name}' не найден. Проверьте наличие файла.")

# Обработчик ошибок
async def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="Произошла ошибка!", exc_info=context.error)
    if update and isinstance(update, Update):
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")

# Основная функция для запуска бота
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('get_id', get_id))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    print("Бот успешно запущен!")
    application.run_polling()

if __name__ == '__main__':
    print("Бот запускается...")
    main()
