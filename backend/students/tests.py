
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient


# Тестирование REST API студентов
class StudentAPITest(TestCase):

    # Подготовка данных перед каждым тестом
    def setUp(self):
        self.client = APIClient()

        # Создание временного JSON-файла
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "students.json"
        self.test_file.write_text("[]", encoding="utf-8")

        # Замена настоящего файла на тестовый
        self.patcher = patch(
            "students.repository.FILE_PATH",
            self.test_file
        )
        self.patcher.start()

        self.addCleanup(self.patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)

        # Данные тестового студента
        self.student = {
            "fullName": "Иванов Иван Иванович",
            "group": "P3224",
            "isuId": 345678,
            "dormNumber": 8,
            "roomNumber": 305,
            "settlementDate": "2025-09-01",
            "isForeigner": False,
            "notes": "Тестовый студент"
        }

    # Получение списка студентов
    def test_get_students(self):
        response = self.client.get("/api/requests")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    # Создание студента
    def test_create_student(self):
        response = self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["isuId"], 345678)

    # Проверка уникальности ИСУ при создании
    def test_duplicate_isu(self):
        self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        response = self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        self.assertEqual(response.status_code, 409)

    # Изменение данных студента
    def test_update_student(self):
        self.client.post("/api/requests", self.student, format="json")

        response = self.client.patch(
            "/api/requests/1",
            {"roomNumber": 410},
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["roomNumber"], 410)

    # Удаление студента
    def test_delete_student(self):
        self.client.post("/api/requests", self.student, format="json")

        response = self.client.delete("/api/requests/1")

        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/requests/1")
        self.assertEqual(response.status_code, 404)

    # Проверка некорректного ИСУ
    def test_invalid_isu(self):
        student = self.student.copy()
        student["isuId"] = 123

        response = self.client.post(
            "/api/requests",
            student,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("isuId", response.data["error"]["details"])

    # Фильтрация через GET
    def test_filter_get(self):
        self.client.post("/api/requests", self.student, format="json")

        response = self.client.get(
            "/api/requests",
            {"group": "P3224"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # Фильтрация через QUERY
    def test_filter_query(self):
        self.client.post("/api/requests", self.student, format="json")

        response = self.client.generic(
            "QUERY",
            "/api/requests",
            data=json.dumps({
                "group": "P3224",
                "dormNumber": 8,
                "isForeigner": False
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # Получение несуществующего студента
    def test_student_not_found(self):
        response = self.client.get("/api/requests/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"]["message"],
            "Студент не найден"
        )

    # Проверка уникальности ИСУ при изменении
    def test_duplicate_isu_on_update(self):
        self.client.post("/api/requests", self.student, format="json")

        second_student = self.student.copy()
        second_student["isuId"] = 456789

        self.client.post("/api/requests", second_student, format="json")

        response = self.client.patch(
            "/api/requests/2",
            {"isuId": 345678},
            format="json"
        )

        self.assertEqual(response.status_code, 409)

    # Проверка запрещённого HTTP-метода
    def test_method_not_allowed(self):
        response = self.client.put(
            "/api/requests/1",
            self.student,
            format="json"
        )

        self.assertEqual(response.status_code, 405)

