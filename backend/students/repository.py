
# Хранение и изменение данных студентов в students.json
import json
from pathlib import Path
import threading
from functools import wraps

# Путь к JSON-файлу
FILE_PATH = Path(__file__).resolve().parent.parent / "students.json"

# Блокировка для безопасной работы с файлом
file_lock = threading.RLock()


# Декоратор для синхронизации функций
def synchronized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with file_lock:
            return func(*args, **kwargs)

    return wrapper


# Получить всех студентов
@synchronized
def get_all_students():
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# Сохранить список студентов в JSON
@synchronized
def save_students(students):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(students, file, ensure_ascii=False, indent=4, default=str)


# Добавить нового студента
@synchronized
def add_student(student_data):
    students = get_all_students()

    # Новый ID = максимальный существующий ID + 1
    new_id = max((student["id"] for student in students), default=0) + 1

    student_data["id"] = new_id
    students.append(student_data)

    save_students(students)

    return student_data


# Найти студента по ID
@synchronized
def get_student_by_id(student_id):
    students = get_all_students()

    for student in students:
        if student["id"] == student_id:
            return student

    return None


# Изменить данные студента
@synchronized
def update_student(student_id, new_data):
    students = get_all_students()

    for student in students:
        if student["id"] == student_id:
            student.update(new_data)
            save_students(students)
            return student

    return None


# Удалить студента по ID
@synchronized
def delete_student(student_id):
    students = get_all_students()

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            save_students(students)
            return True

    return False
