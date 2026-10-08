
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, APIException


# Ошибка: студент с таким ИСУ уже существует
class StudentAlreadyExists(APIException):
    status_code = 409
    default_detail = "Студент с таким ИСУ ID уже существует"
    default_code = "student_already_exists"


# Ошибка: запрос невозможно обработать
class UnprocessableEntity(APIException):
    status_code = 422
    default_detail = "Запрос невозможно обработать"
    default_code = "unprocessable_entity"


# Общий обработчик исключений REST API
def custom_exception_handler(exc, context):
    # Получаем стандартный ответ DRF
    response = exception_handler(exc, context)

    # Неизвестные исключения передаём Django
    if response is None:
        return None

    # Ошибки валидации данных
    if isinstance(exc, ValidationError):
        details = {}

        # Собираем первую ошибку для каждого поля
        for field, errors in response.data.items():
            if isinstance(errors, list):
                details[field] = str(errors[0])
            else:
                details[field] = str(errors)

        response.data = {
            "error": {
                "message": "Ошибка валидации",
                "details": details
            }
        }

    # Ошибка повторяющегося номера ИСУ
    elif isinstance(exc, StudentAlreadyExists):
        response.data = {
            "error": {
                "message": str(exc.detail),
                "details": {
                    "isuId": "Номер ИСУ должен быть уникальным"
                }
            }
        }

    # Остальные исключения DRF, например 404
    else:
        message = response.data.get("detail", "Ошибка запроса")

        response.data = {
            "error": {
                "message": str(message),
                "details": {}
            }
        }

    return response
