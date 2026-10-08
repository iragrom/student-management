from django.apps import AppConfig

# Настройки приложения students
class StudentsConfig(AppConfig):
    # Тип автоматически создаваемого первичного ключа
    default_auto_field = 'django.db.models.BigAutoField'

    # Имя приложения
    name = 'students'
