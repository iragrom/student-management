
from dataclasses import dataclass, asdict
from datetime import date

#Гарантирует, что объект студента, создаваемый внутри приложения,
#соответствует установленным ограничениям
@dataclass(frozen=True) #после создания объекта нельзя обычным присваиванием изменять его поля
class Student:
    id: int
    fullName: str
    group: str
    isuId: int
    dormNumber: int
    roomNumber: int
    settlementDate: date
    isForeigner: bool
    notes: str = ""

    def __post_init__(self):
        # Проверка ID
        if type(self.id) is not int or self.id <= 0:
            raise ValueError(
                "ID должен быть положительным целым числом"
            )

        # Проверка ФИО
        if not isinstance(self.fullName, str):
            raise ValueError("ФИО должно быть строкой")

        name = self.fullName.strip()

        if not 2 <= len(name) <= 100:
            raise ValueError(
                "ФИО должно содержать от 2 до 100 символов"
            )

        if not any(char.isalpha() for char in name):
            raise ValueError("ФИО должно содержать буквы")

        if not all(
            char.isalpha() or char in " -"
            for char in name
        ):
            raise ValueError(
                "ФИО может содержать только буквы, пробелы и дефисы"
            )

        # Проверка группы
        if (
            not isinstance(self.group, str)
            or len(self.group) != 5
            or not self.group[0].isalpha()
            or not all(
                char in "0123456789"
                for char in self.group[1:]
            )
        ):
            raise ValueError(
                "Группа должна состоять из буквы и четырёх цифр"
            )

        # Проверка номера ИСУ
        if (
            type(self.isuId) is not int
            or not 100000 <= self.isuId <= 999999
        ):
            raise ValueError(
                "ИСУ должен состоять из шести цифр"
            )

        # Проверка общежития
        if (
            type(self.dormNumber) is not int
            or not 1 <= self.dormNumber <= 10
        ):
            raise ValueError(
                "Номер общежития должен быть от 1 до 10"
            )

        # Проверка комнаты
        if (
            type(self.roomNumber) is not int
            or not 100 <= self.roomNumber <= 999
        ):
            raise ValueError(
                "Номер комнаты должен быть от 100 до 999"
            )

        # Проверка даты заселения
        if not isinstance(self.settlementDate, date):
            raise ValueError(
                "Дата заселения должна быть датой"
            )

        today = date.today()

        if not 2018 <= self.settlementDate.year <= 2035:
            raise ValueError(
                "Год заселения должен быть от 2018 до 2035"
            )

        if self.settlementDate > today:
            raise ValueError(
                "Дата заселения не может быть в будущем"
            )

        if self.settlementDate.year < today.year - 10:
            raise ValueError(
                "Дата заселения не может быть старше 10 лет"
            )

        # Проверка иностранного студента
        if type(self.isForeigner) is not bool:
            raise ValueError(
                "Поле isForeigner должно быть булевым"
            )

        # Проверка заметок
        if not isinstance(self.notes, str):
            raise ValueError(
                "Заметки должны быть строкой"
            )

        if len(self.notes) > 500:
            raise ValueError(
                "Заметки не могут превышать 500 символов"
            )

        if len(self.notes.split()) > 50:
            raise ValueError(
                "Заметки не могут содержать больше 50 слов"
            )

        forbidden_chars = "/\\*\"<>"

        if any(char in self.notes for char in forbidden_chars):
            raise ValueError(
                "Заметки содержат запрещённые символы"
            )
    #Cоздаёт объект Student из словаря
    @classmethod
    def from_dict(cls, data):
        values = dict(data)

        if isinstance(values["settlementDate"], str):
            values["settlementDate"] = date.fromisoformat(
                values["settlementDate"]
            )

        return cls(**values)

    def to_dict(self):
        values = asdict(self)
        values["settlementDate"] = (
            self.settlementDate.isoformat()
        )
        return values
