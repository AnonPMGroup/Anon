from django.apps import AppConfig
import threading
from .bot_logic import main  # Импортируйте функцию запуска бота

class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        # Запускаем бота в отдельном потоке
        threading.Thread(target=main, daemon=True).start()
