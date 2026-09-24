//Запуск

//Когда HTML-страница полностью будет построена браузером, выполни функцию.
//Определяем какая страница открыта.
document.addEventListener("DOMContentLoaded", function () {

    const table = document.getElementById("student-table-body");
    const form = document.getElementById("student-form");
    const profile = document.getElementById("profile-content");

    if (table !== null) {
        showStudentsTable();
    }

    if (profile !== null) {
        showStudentProfile();
    }

    if (form !== null) {
        startForm();
    }
});

function startForm() {
    const form = document.getElementById("student-form");

    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (id !== null) {
        fillForm(id); //заполнить данными студента для редактирования
    }

    //Ждем, когда  пользователь отправит форму
    form.addEventListener("submit", function (e) {
        e.preventDefault(); //предотвращает стандартную отправку формы

        if (validateForm() === false) {
            return;
        }

        saveForm(id);
    });
}

//Собрать значения из HTML-формы в объект student
//и создаем нового или обновляем существующего студента.
function saveForm(id) {

    const student = {
        fullName: document.getElementById("form-fullname").value,
        group: document.getElementById("form-group").value,
        isuId: Number(document.getElementById("form-isuid").value),
        dormNumber: Number(document.getElementById("form-dorm").value),
        roomNumber: Number(document.getElementById("form-room").value),
        moveInDate: document.getElementById("form-movein").value,
        isForeigner: document.getElementById("form-foreigner").checked,
        notes: document.getElementById("form-notes").value
    };

    if (id === null) {
        createStudent(student);//новый
    } else {
        updateStudent(id, student);//существующий
    }

    window.location.href = "index.html"; //перейти на страницу index.html
}

//Получить существующего студента и подставить его данные в поля формы
function fillForm(id) {
    const student = getStudentById(id);

    if (student === null) {
        alert("Студент не найден");
        window.location.href = "index.html";
        return;
    }

    document.getElementById("form-student-id").value = student.id;
    document.getElementById("form-fullname").value = student.fullName;
    document.getElementById("form-group").value = student.group;
    document.getElementById("form-isuid").value = student.isuId;
    document.getElementById("form-dorm").value = student.dormNumber;
    document.getElementById("form-room").value = student.roomNumber;
    document.getElementById("form-movein").value = student.moveInDate;
    document.getElementById("form-foreigner").checked = student.isForeigner;
    document.getElementById("form-notes").value = student.notes;
}