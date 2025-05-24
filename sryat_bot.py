from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище ID пользователей
users = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    users.add(user_id)
    
    keyboard = [[InlineKeyboardButton("Гулять", callback_data='walk')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text('Привет! Нажми кнопку "Гулять", чтобы позвать всех гулять.', reply_markup=reply_markup)

# Обработка кнопки "Гулять"
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    user_name = user.first_name
    
    if query.data == 'walk':
        for user_id in users:
            try:
                keyboard = [
                    [
                        InlineKeyboardButton("Да", callback_data=f'yes_{user.id}'),
                        InlineKeyboardButton("Нет", callback_data=f'no_{user.id}'),
                    ],
                    [
                        InlineKeyboardButton("Не знаю", callback_data=f'idk_{user.id}'),
                        InlineKeyboardButton("Потом", callback_data=f'later_{user.id}'),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"{user_name} зовёт гулять! Пойдёшь?",
                    reply_markup=reply_markup
                )
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

# Обработка ответов
async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    data = query.data
    responding_user = update.effective_user.first_name
    target_user_id = int(data.split('_')[1])
    
    if data.startswith('yes_'):
        response = "Да"
    elif data.startswith('no_'):
        response = "Нет"
    elif data.startswith('idk_'):
        response = "Не знаю"
    elif data.startswith('later_'):
        response = "Потом"
    else:
        response = "???"
    
    try:
        await context.bot.send_message(
            chat_id=target_user_id,
            text=f"{responding_user} ответил(а): {response}"
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке ответа пользователю {target_user_id}: {e}")

def main() -> None:
    # Замените 'YOUR_BOT_TOKEN' на реальный токен
    application = Application.builder().token("7680859012:AAEDaVj3arrWhcW8QG1ChowE4TMnuYur_KI").build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click, pattern='^walk$'))
    application.add_handler(CallbackQueryHandler(handle_response, pattern='^(yes|no|idk|later)_'))
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
