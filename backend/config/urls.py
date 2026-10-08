
"""
Настройка маршрутов Django-проекта.

Здесь указываются URL-адреса и обработчики,
которые должны отвечать на поступающие HTTP-запросы.
"""

from django.contrib import admin
from django.urls import path, include

# Список маршрутов проекта
urlpatterns = [
    # Адрес встроенной панели администратора Django
    path('admin/', admin.site.urls),

    # Все запросы с  /api/ передаются
    # в файл students/urls.py
    path('api/', include('students.urls')),
]

