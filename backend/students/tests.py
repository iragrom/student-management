
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient


class StudentAPITest(TestCase):

    # Подготовка перед каждым тестом
    def setUp(self):
        self.client = APIClient()

        # Временный JSON-файл
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "students.json"
        self.test_file.write_text("[]", encoding="utf-8")

        # Подменяем настоящий файл тестовым
        self.patcher = patch(
            "students.repository.FILE_PATH",
            self.test_file
        )
        self.patcher.start()

        self.addCleanup(self.patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)

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

    # 1. Получение пустого списка
    def test_get_students(self):
        response = self.client.get("/api/requests")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    # 2. Создание студента
    def test_create_student(self):
        response = self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["isuId"], 345678)
        self.assertEqual(response.data["id"], 1)

    # 3. Уникальность ИСУ при создании
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

    # 4. Изменение студента
    def test_update_student(self):
        self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        response = self.client.patch(
            "/api/requests/1",
            {"roomNumber": 410},
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["roomNumber"], 410)

    # 5. Удаление студента
    def test_delete_student(self):
        self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        response = self.client.delete("/api/requests/1")

        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/requests/1")
        self.assertEqual(response.status_code, 404)

    # 6. Некорректный ИСУ
    def test_invalid_isu(self):
        student = self.student.copy()
        student["isuId"] = 123

        response = self.client.post(
            "/api/requests",
            student,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "isuId",
            response.data["error"]["details"]
        )

    # 7. Фильтрация через GET
    def test_filter_get(self):
        self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        response = self.client.get(
            "/api/requests",
            {"group": "P3224"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # 8. Фильтрация через QUERY
    def test_filter_query(self):
        self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

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

    # 9. Несуществующий студент
    def test_student_not_found(self):
        response = self.client.get("/api/requests/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"]["message"],
            "Студент не найден"
        )

    # 10. Уникальность ИСУ при обновлении
    def test_duplicate_isu_on_update(self):
        self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        second_student = self.student.copy()
        second_student["isuId"] = 456789

        self.client.post(
            "/api/requests",
            second_student,
            format="json"
        )

        response = self.client.patch(
            "/api/requests/2",
            {"isuId": 345678},
            format="json"
        )

        self.assertEqual(response.status_code, 409)

    # 11. Запрещённый HTTP-метод
    def test_method_not_allowed(self):
        response = self.client.put(
            "/api/requests/1",
            self.student,
            format="json"
        )

        self.assertEqual(response.status_code, 405)

    # 12. Автоматическая генерация ID
    def test_auto_generated_id(self):
        first = self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        second_student = self.student.copy()
        second_student["isuId"] = 456789

        second = self.client.post(
            "/api/requests",
            second_student,
            format="json"
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(first.data["id"], 1)
        self.assertEqual(second.data["id"], 2)

    # 13. PATCH сохраняет остальные поля
    def test_patch_preserves_other_fields(self):
        self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        response = self.client.patch(
            "/api/requests/1",
            {"roomNumber": 410},
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["roomNumber"], 410)
        self.assertEqual(
            response.data["fullName"],
            self.student["fullName"]
        )
        self.assertEqual(response.data["isuId"], 345678)

    # 14. Некорректный PATCH не изменяет данные
    def test_invalid_patch_preserves_student(self):
        self.client.post(
            "/api/requests",
            self.student,
            format="json"
        )

        response = self.client.patch(
            "/api/requests/1",
            {"roomNumber": -5},
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "roomNumber",
            response.data["error"]["details"]
        )

        saved = self.client.get("/api/requests/1")

        self.assertEqual(saved.status_code, 200)
        self.assertEqual(saved.data["roomNumber"], 305)

    # 15. Некорректное имя студента
    def test_invalid_full_name(self):
        student = self.student.copy()
        student["fullName"] = "12345"

        response = self.client.post(
            "/api/requests",
            student,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "fullName",
            response.data["error"]["details"]
        )


