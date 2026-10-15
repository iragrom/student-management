from .models import Student
import json
import os
import tempfile
import threading

from datetime import date, datetime
from functools import wraps
from pathlib import Path


# Путь к файлу хранения студентов
FILE_PATH = (
    Path(__file__).resolve().parent.parent / "students.json"
)

# Блокировка для потоков одного процесса
file_lock = threading.RLock()


# Декоратор для синхронизации доступа к файлу
def synchronized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with file_lock:
            return func(*args, **kwargs)

    return wrapper


# Преобразование значений для JSON
def json_converter(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()

    raise TypeError(
        f"Тип {type(value).__name__} нельзя записать в JSON"
    )


# Получение всех студентов
@synchronized
def get_all_students():
    if not FILE_PATH.exists():
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        students = json.load(file) #читает JSON и преобразует его в Python-объект

    if not isinstance(students, list): #проверяем, что в файле хранится список
        raise ValueError(
            "Файл students.json должен содержать список"
        )

    return students


# Сохранение списка студентов
@synchronized
def save_students(students):
    FILE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True #не вызывает ошибку, если папка уже существует
    )

    temp_path = None

    try:
        # Создаём временный файл в той же папке
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=FILE_PATH.parent, #создать рядом с students.json
            prefix=".students-",
            suffix=".tmp",
            delete=False
        ) as file:

            temp_path = Path(file.name)
            #Запись JSON
            json.dump(
                students,
                file,
                ensure_ascii=False, #для русских букв
                indent=4,
                default=json_converter #date в стороки
            )

            file.flush() #передаёт данные из буфера Python операционной системе
            os.fsync(file.fileno()) #завершить запись данных файла на устройство хранения

        # Заменяем старый файл новым
        os.replace(temp_path, FILE_PATH)

    finally:
        # Удаляем временный файл при ошибке
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


# Добавление нового студента

@synchronized
def add_student(student_data):
    students = get_all_students()

    new_id = max(
        (student["id"] for student in students),
        default=0
    ) + 1

    new_student = Student.from_dict({
        **student_data,
        "id": new_id
    })

    new_student_data = new_student.to_dict()

    students.append(new_student_data)
    save_students(students)

    return new_student_data



# Получение студента по ID
@synchronized
def get_student_by_id(student_id):
    students = get_all_students()

    for student in students:
        if student["id"] == student_id:
            return student

    return None


# Обновление студента
@synchronized
def update_student(student_id, new_data):
    students = get_all_students()

    for index, student in enumerate(students):
        if student["id"] == student_id:

            changes = {
                key: value
                for key, value in new_data.items()
                if key != "id"
            }

            updated_data = {
                **student,
                **changes
            }

            updated_student = Student.from_dict(updated_data)

            students[index] = updated_student.to_dict()
            save_students(students)

            return students[index]

    return None



# Удаление студента
@synchronized
def delete_student(student_id):
    students = get_all_students()

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            save_students(students)
            return True

    return False

