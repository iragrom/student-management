
#!/usr/bin/env python
"""Управление проектом Django."""

import os
import sys


def main():
    """Выполнение команд Django."""

    # Указываем файл настроек проекта
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        # Импорт функции для выполнения команд Django
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        # Ошибка, если Django не установлен или недоступен
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Выполнение команды из терминала
    execute_from_command_line(sys.argv)


# Запуск главной функции
if __name__ == '__main__':
    main()

