
from .repository import (
    get_all_students,
    get_student_by_id,
    add_student,
    update_student,
    delete_student,
    file_lock
)


# Получение списка студентов с фильтрацией
def get_students(filters):
    students = get_all_students()
    return filter_students(students, filters)


# Получение студента по ID
def get_student(student_id):
    return get_student_by_id(student_id)


# Создание студента с проверкой уникальности ИСУ
def create_student(data):
    with file_lock:
        students = get_all_students()

        for student in students:
            if student["isuId"] == data["isuId"]:
                return None

        return add_student(data)


# Изменение студента с проверкой уникальности ИСУ
def edit_student(student_id, data):
    with file_lock:
        students = get_all_students()

        for student in students:
            if student["isuId"] == data.get("isuId") and student["id"] != student_id:
                return None

        return update_student(student_id, data)


# Удаление студента
def remove_student(student_id):
    return delete_student(student_id)


# Фильтрация студентов по заданным полям
def filter_students(students, filters):
    for field, value in filters.items():
        students = [
            student for student in students
            if str(student.get(field, "")).lower() == str(value).lower()
        ]

    return students
