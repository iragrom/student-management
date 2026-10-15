#Бизнес-логика
from rest_framework.exceptions import ValidationError, NotFound

from .exceptions import StudentAlreadyExists
from .models import Student
from .repository import (
    get_all_students,
    get_student_by_id,
    add_student,
    update_student as repository_update_student,
    delete_student,
    file_lock,
)


def get_students(filters):
    students = get_all_students()
    filtered_students = filter_students(students, filters)

    return [
        Student.from_dict(student)
        for student in filtered_students
    ]


def get_student(student_id):
    student_data = get_student_by_id(student_id)

    if student_data is None:
        raise NotFound("Студент не найден")

    return Student.from_dict(student_data)


def create_student(data):
    with file_lock:
        students = get_all_students()

        if any(
            student["isuId"] == data["isuId"]
            for student in students
        ):
            raise StudentAlreadyExists()

        student_data = add_student(data)

        return Student.from_dict(student_data)


def update_student(student_id, data):
    with file_lock:
        students = get_all_students()

        existing_student = next(
            (
                student
                for student in students
                if student["id"] == student_id
            ),
            None,
        )

        if existing_student is None:
            raise NotFound("Студент не найден")

        if "isuId" in data:
            if any(
                student["isuId"] == data["isuId"]
                and student["id"] != student_id
                for student in students
            ):
                raise StudentAlreadyExists()

        updated_data = repository_update_student(
            student_id,
            data
        )

        if updated_data is None:
            raise NotFound("Студент не найден")

        return Student.from_dict(updated_data)


def remove_student(student_id):
    with file_lock:
        deleted = delete_student(student_id)

        if not deleted:
            raise NotFound("Студент не найден")

        return deleted


def filter_students(students, filters):
    allowed_fields = set(Student.__dataclass_fields__) - {"id"}  #содержит все поля модели, кроме id

    numeric_fields = {
        "isuId",
        "dormNumber",
        "roomNumber",
    }

    for field, value in filters.items():
        if field not in allowed_fields:
            raise ValidationError({
                field: ["Неизвестное поле фильтрации"]
            })

        if field == "isForeigner":
            normalized = str(value).strip().lower()

            if normalized in ("true", "1"):
                expected = True
            elif normalized in ("false", "0"):
                expected = False
            else:
                raise ValidationError({
                    field: ["Ожидается true или false"]
                })

            students = [
                student
                for student in students
                if student.get(field) is expected
            ]

        elif field in numeric_fields:
            if (
                isinstance(value, bool)
                or isinstance(value, float)
                or not str(value).strip().isdigit()
            ):
                raise ValidationError({
                    field: ["Ожидается целое число"]
                })

            expected = int(value)

            students = [
                student
                for student in students
                if student.get(field) == expected
            ]

        else:
            expected = str(value).strip().lower()

            students = [
                student
                for student in students
                if str(student.get(field, "")).strip().lower()
                == expected
            ]

    return students




