
"""
Настройка WSGI для Django-проекта.

WSGI обеспечивает взаимодействие между веб-сервером
и Django-приложением при обработке HTTP-запросов.
"""

import os

from django.core.wsgi import get_wsgi_application

# Указываем файл настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаём WSGI-приложение
application = get_wsgi_application()
