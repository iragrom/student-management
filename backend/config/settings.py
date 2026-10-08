
"""
Настройки Django-проекта config.

Файл создан автоматически при создании проекта Django.
Здесь настраиваются приложения, обработка запросов,
безопасность, база данных и другие параметры.

Документация:
https://docs.djangoproject.com/en/5.2/topics/settings/
"""
import os

from pathlib import Path

# Путь к корневой папке backend
BASE_DIR = Path(__file__).resolve().parent.parent


# Настройки для разработки

# Секретный ключ Django
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Показывать подробные ошибки во время разработки
DEBUG = True

# Список разрешённых имён хостов
ALLOWED_HOSTS = []


# Подключённые приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',  # Создание REST API
    'corsheaders',     # Разрешение запросов от frontend
    'students',        # Приложение для работы со студентами
]


# Промежуточные обработчики HTTP-запросов и ответов
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Главный файл маршрутов проекта
ROOT_URLCONF = 'config.urls'


# Настройки шаблонов Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Точка входа для WSGI-сервера
WSGI_APPLICATION = 'config.wsgi.application'


# Настройки базы данных SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Проверки надёжности паролей в Django
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Язык и часовой пояс
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

# Поддержка перевода интерфейса Django
USE_I18N = True

# Использование часовых поясов
USE_TZ = True


# Адрес для статических файлов (CSS, JS, изображения)
STATIC_URL = 'static/'


# Тип автоматически создаваемого первичного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Адреса frontend, которым разрешено обращаться к backend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]


# Разрешённые HTTP-методы для междоменных запросов
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "QUERY",
]


# Настройки Django REST Framework
REST_FRAMEWORK = {
    # Наш обработчик ошибок API
    "EXCEPTION_HANDLER": "students.exceptions.custom_exception_handler"
}
