//Проверка формы данных

function validateForm() {
    const fullName = document.getElementById("form-fullname");
    const group = document.getElementById("form-group");
    const isuId = document.getElementById("form-isuid");
    const dorm = document.getElementById("form-dorm");
    const room = document.getElementById("form-room");
    const moveIn = document.getElementById("form-movein");
    const notes = document.getElementById("form-notes");

    // Убираем старые ошибки
    document.getElementById("error-fullname").textContent = "";
    document.getElementById("error-group").textContent = "";
    document.getElementById("error-isuid").textContent = "";
    document.getElementById("error-isuid-unique").textContent = "";
    document.getElementById("error-dorm").textContent = "";
    document.getElementById("error-room").textContent = "";
    document.getElementById("error-movein").textContent = "";
    document.getElementById("error-notes").textContent = "";

    let isValid = true;


    // ФИО
    if (fullName.checkValidity() === false) {
        document.getElementById("error-fullname").textContent =
            "Введите корректное ФИО";

        isValid = false;
    }


    // Группа
    if (group.checkValidity() === false) {
        document.getElementById("error-group").textContent =
            "Введите группу в формате P3224";

        isValid = false;
    }


    // ИСУ
    if (isuId.checkValidity() === false) {
        document.getElementById("error-isuid").textContent =
            "ИСУ ID должен быть целым числом от 100000 до 999999";

        isValid = false;
    }


    // Проверка уникальности ИСУ
    if (isuId.value !== "") {
        const students = getAllStudents();

        const params = new URLSearchParams(window.location.search);
        const currentId = params.get("id");

        for (let i = 0; i < students.length; i++) {

            if (
                students[i].isuId === Number(isuId.value) &&
                students[i].id !== Number(currentId)
            ) {
                document.getElementById("error-isuid-unique").textContent =
                    "Студент с таким ИСУ ID уже существует";

                isValid = false;
            }
        }
    }


    // Общежитие
    if (dorm.checkValidity() === false) {
        document.getElementById("error-dorm").textContent =
            "Номер общежития должен быть целым числом от 1 до 10";

        isValid = false;
    }


    // Комната
    if (room.checkValidity() === false) {
        document.getElementById("error-room").textContent =
            "Номер комнаты должен быть целым числом от 100 до 999";

        isValid = false;
    }


    // Дата заселения
    if (moveIn.checkValidity() === false) {
        document.getElementById("error-movein").textContent =
            "Дата заселения должна быть в диапазоне 2018–2035";

        isValid = false;
    }


    // Студент не может жить в общежитии больше 10 лет
    if (moveIn.value !== "") {
        const moveInDate = new Date(moveIn.value);

        const today = new Date();

        const tenYearsAgo = new Date();
        tenYearsAgo.setFullYear(today.getFullYear() - 10);

        if (moveInDate < tenYearsAgo) {
            document.getElementById("error-movein").textContent =
                "Студент не может жить в общежитии больше 10 лет";

            isValid = false;
        }
    }


    // Заметки: запрещённые символы
    const forbiddenSymbols = ["/", "\\", "\"", "'", "<", ">"];

    for (let i = 0; i < forbiddenSymbols.length; i++) {

        if (notes.value.includes(forbiddenSymbols[i])) {
            document.getElementById("error-notes").textContent =
                "В заметках нельзя использовать / \\ \" ' < >";

            isValid = false;
        }
    }


    // Заметки: не больше 500 символов
    if (notes.value.length > 500) {
        document.getElementById("error-notes").textContent =
            "В заметках должно быть не больше 500 символов";

        isValid = false;
    }


    // Заметки: не больше 50 слов
    const notesText = notes.value.trim();

    if (notesText !== "") {
        const words = notesText.split(/\s+/);

        if (words.length > 50) {
            document.getElementById("error-notes").textContent =
                "В заметках должно быть не больше 50 слов";

            isValid = false;
        }
    }


    return isValid;
}