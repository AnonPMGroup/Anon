from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.contrib.auth import get_user_model


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я ваш Telegram-бот.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Доступные команды: /start, /help")

def list_users(update: Update, context: CallbackContext):
    User = get_user_model()
    users = User.objects.all()  
    if not users:
        update.message.reply_text("ггвп.")
    else:
        user_list = "\n".join([f"name:{user.username}, registered date:{user.date_joined}" for user in users])
        update.message.reply_text(f"\n{user_list}")

def main():
    updater = Updater("8043510535:AAEtcb3SIXZZTD5JTfexYB-JqbCPZEvqXHA")
    dispatcher = updater.dispatcher

    # Регистрация команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("users", list_users))

    # Запуск бота
    updater.start_polling()
    print("Telegram-бот запущен!")

