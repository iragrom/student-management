
from datetime import date

from rest_framework import serializers


# Проверка данных студента
class StudentSerializer(serializers.Serializer):
    fullName = serializers.CharField(min_length=2, max_length=100)
    group = serializers.CharField(max_length=5)
    isuId = serializers.IntegerField(min_value=100000, max_value=999999)
    dormNumber = serializers.IntegerField(min_value=1, max_value=10)
    roomNumber = serializers.IntegerField(min_value=100, max_value=999)
    settlementDate = serializers.DateField()
    isForeigner = serializers.BooleanField()
    notes = serializers.CharField(
        max_length=500,
        allow_blank=True,
        required=False,
        default=""
    )

    # Проверка ФИО
    def validate_fullName(self, value):
        name = value.replace(" ", "").replace("-", "")

        if not name or not name.isalpha():
            raise serializers.ValidationError(
                "ФИО может содержать только буквы, пробелы и дефисы"
            )

        return value

    # Проверка учебной группы
    def validate_group(self, value):
        if (
            len(value) != 5
            or not value[0].isalpha()
            or not all(char in "0123456789" for char in value[1:])
        ):
            raise serializers.ValidationError(
                "Группа должна состоять из буквы и четырёх цифр"
            )

        return value.upper()

    # Проверка даты заселения
    def validate_settlementDate(self, value):
        today = date.today()

        if value.year < 2018 or value.year > 2035:
            raise serializers.ValidationError(
                "Год заселения должен быть от 2018 до 2035"
            )

        if value > today:
            raise serializers.ValidationError(
                "Дата заселения не может быть в будущем"
            )

        if value.year < today.year - 10:
            raise serializers.ValidationError(
                "Дата заселения не может быть старше 10 лет"
            )

        return value

    # Проверка заметок
    def validate_notes(self, value):
        if len(value.split()) > 50:
            raise serializers.ValidationError(
                "Заметки не могут содержать больше 50 слов"
            )

        forbidden_chars = '/\\"\'<>'

        if any(char in value for char in forbidden_chars):
            raise serializers.ValidationError(
                "Заметки содержат запрещённые символы"
            )

        return value
