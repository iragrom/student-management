from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import StudentSerializer
from .services import (
    get_students,
    get_student,
    create_student,
    update_student,
    remove_student,
)

#Класс отвечает за работу со всем списком студентов по адресу /api/requests.
class StudentListView(APIView):
    http_method_names = ["get", "post", "query", "options"]

    # GET
    def get(self, request):
        students = get_students(request.query_params)

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # QUERY
    def query(self, request):
        if not isinstance(request.data, dict):
            raise ValidationError({
                "filters": ["Ожидается JSON-объект с параметрами фильтрации"]
            })

        students = get_students(request.data)

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  #запускает проверки Serializer

        student = create_student(serializer.validated_data)

        return Response(
            StudentSerializer(student).data,
            status=status.HTTP_201_CREATED
        )

#Класс отвечает за операции с одним студентом по адресу /api/requests/<id>.
class StudentDetailView(APIView):
    http_method_names = ["get", "patch", "delete", "options"]

    # GET
    def get(self, request, student_id):
        student = get_student(student_id)

        return Response(
            StudentSerializer(student).data,
            status=status.HTTP_200_OK
        )

    # PATCH
    def patch(self, request, student_id):
        student = get_student(student_id)

        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        updated_student = update_student(
            student_id,
            serializer.validated_data
        )

        return Response(
            StudentSerializer(updated_student).data,
            status=status.HTTP_200_OK
        )

    # DELETE
    def delete(self, request, student_id):
        remove_student(student_id)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )



