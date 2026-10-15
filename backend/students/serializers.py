#Проверяет данные, которые приходят от клиента
from datetime import date
from rest_framework import serializers
from .models import Student

#Cобственный класс сериализатора
class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) #поле доступно для вывода

    fullName = serializers.CharField(   #строковое поле
        min_length=2,
        max_length=100
    )

    group = serializers.CharField(max_length=5)

    isuId = serializers.IntegerField(
        min_value=100000,
        max_value=999999
    )

    dormNumber = serializers.IntegerField(
        min_value=1,
        max_value=10
    )

    roomNumber = serializers.IntegerField(
        min_value=100,
        max_value=999
    )

    settlementDate = serializers.DateField() #для календарных дат

    isForeigner = serializers.BooleanField() #поле логического типа

    notes = serializers.CharField(
        max_length=500,
        allow_blank=True, #разрешает пустую строку
        required=False, #поле необязательно передавать во входных данных
        default=""
    )

    # Проверка ФИО
    def validate_fullName(self, value):
        name = value.strip()

        if not any(char.isalpha() for char in name):
            raise serializers.ValidationError(
                "ФИО должно содержать буквы"
            )

        if not all(
            char.isalpha() or char in " -"
            for char in name
        ):
            raise serializers.ValidationError(
                "ФИО может содержать только буквы, пробелы и дефисы"
            )

        return name

    # Проверка группы
    def validate_group(self, value):
        group = value.upper()

        if (
            len(group) != 5
            or not group[0].isalpha()
            or not all(char in "0123456789" for char in group[1:])
        ):
            raise serializers.ValidationError(
                "Группа должна состоять из буквы и четырёх цифр"
            )

        return group

    # Проверка даты заселения
    def validate_settlementDate(self, value):
        today = date.today()

        if not 2018 <= value.year <= 2035:
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

        forbidden_chars = "/\\*\"<>"

        if any(char in value for char in forbidden_chars):
            raise serializers.ValidationError(
                "Заметки содержат запрещённые символы"
            )

        return value

    # Преобразование модели Student в JSON-представление
    def to_representation(self, instance):
        if isinstance(instance, Student):
            instance = instance.to_dict()

        return super().to_representation(instance)



