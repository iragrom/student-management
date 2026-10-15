
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, ValidationError


class StudentAlreadyExists(APIException):
    status_code = 409
    default_detail = "Студент с таким ИСУ уже существует"
    default_code = "student_already_exists"


def normalize_errors(value):
    if isinstance(value, dict):
        return {
            str(key): normalize_errors(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            normalize_errors(item)
            for item in value
        ]

    return str(value)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, ValidationError):
        details = normalize_errors(exc.detail)

        if isinstance(details, dict):
            messages = []

            for field, errors in details.items():
                if not isinstance(errors, list):
                    errors = [errors]

                for error in errors:
                    messages.append(
                        f"Поле '{field}': {error}"
                    )

            message = "; ".join(messages)

        elif isinstance(details, list):
            message = "; ".join(str(error) for error in details)

        else:
            message = str(details)

    else:
        message = str(exc.detail)
        details = {}

        if isinstance(exc, StudentAlreadyExists):
            details = {
                "isuId": [
                    "Номер ИСУ должен быть уникальным"
                ]
            }

    response.data = {
        "error": {
            "message": message,
            "details": details
        }
    }

    return response


