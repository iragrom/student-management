"""
Настройка ASGI для проекта Django.

Переменная application используется ASGI-сервером
для запуска приложения.

Подробнее:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application() #создаёт объект приложения, который будет обрабатывать запросы через ASGI
