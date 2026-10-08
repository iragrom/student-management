
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .exceptions import StudentAlreadyExists
from .serializers import StudentSerializer
from .services import (
    get_students,
    get_student,
    create_student,
    edit_student,
    remove_student
)


# Работа со списком студентов
class StudentListView(APIView):
    http_method_names = ["get", "post", "query", "options"]

    # Получение списка студентов с фильтрацией
    def get(self, request):
        students = get_students(request.query_params)
        return Response(students, status=status.HTTP_200_OK)

    # Фильтрация по параметрам из тела запроса
    def query(self, request):
        students = get_students(request.data)
        return Response(students, status=status.HTTP_200_OK)

    # Создание студента
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = create_student(serializer.validated_data)

        if student is None:
            raise StudentAlreadyExists()

        return Response(student, status=status.HTTP_201_CREATED)


# Работа с конкретным студентом
class StudentDetailView(APIView):

    # Получение студента по ID
    def get(self, request, student_id):
        student = get_student(student_id)

        if student is None:
            raise NotFound("Студент не найден")

        return Response(student, status=status.HTTP_200_OK)

    # Частичное изменение студента
    def patch(self, request, student_id):
        student = get_student(student_id)

        if student is None:
            raise NotFound("Студент не найден")

        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        updated_student = edit_student(
            student_id,
            serializer.validated_data
        )

        if updated_student is None:
            raise StudentAlreadyExists()

        return Response(updated_student, status=status.HTTP_200_OK)

    # Удаление студента
    def delete(self, request, student_id):
        deleted = remove_student(student_id)

        if not deleted:
            raise NotFound("Студент не найден")

        return Response(status=status.HTTP_204_NO_CONTENT)



