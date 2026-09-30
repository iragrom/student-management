//Запуск

//Когда HTML-страница полностью будет построена браузером, выполни функцию.
//Определяем какая страница открыта.
document.addEventListener("DOMContentLoaded", function () {

    const table = document.getElementById("student-table-body");
    const form = document.getElementById("student-form");
    const profile = document.getElementById("profile-content");

    if (table !== null) {
        showStudentsTable();
        startFilters(); //новая панель фильтров на index.html
    }

    if (profile !== null) {
        showStudentProfile();
    }

    if (form !== null) {
        startForm();
    }
});

//Запуск обработчиков фильтров
function startFilters() {
    const applyBtn = document.getElementById("btn-filter-apply");
    const resetBtn = document.getElementById("btn-filter-reset");
    const toggleBtn = document.getElementById("btn-filter-toggle");

    //Кнопка "Применить" — перерисовать таблицу с учётом фильтров
    if (applyBtn !== null) {
        applyBtn.addEventListener("click", function () {
            showStudentsTable();
        });
    }

    //Кнопка "Сбросить" — очистить поля и перерисовать
    if (resetBtn !== null) {
        resetBtn.addEventListener("click", function () {
            clearFilters();
            showStudentsTable();
        });
    }

    //Кнопка "Расширенный фильтр" — раскрыть/скрыть дополнительные поля
    if (toggleBtn !== null) {
        toggleBtn.addEventListener("click", toggleAdvancedFilters);
    }
}

//Запуск формы (создание или редактирование)
function startForm() {
    const form = document.getElementById("student-form");

    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (id !== null) {
        fillForm(id); //заполнить данными студента для редактирования
    }

    //Ждем, когда  пользователь отправит форму
    form.addEventListener("submit", async function (e) {
        e.preventDefault(); //предотвращает стандартную отправку формы

        if (validateForm() === false) {
            return;
        }

        await saveForm(id);
    });
}

//Собрать значения из HTML-формы в объект student
//и создаем нового или обновляем существующего студента.
async function saveForm(id) {

    const student = {
        fullName: document.getElementById("form-fullname").value,
        group: document.getElementById("form-group").value,
        isuId: Number(document.getElementById("form-isuid").value),
        dormNumber: Number(document.getElementById("form-dorm").value),
        roomNumber: Number(document.getElementById("form-room").value),
        settlementDate: document.getElementById("form-movein").value,
        isForeigner: document.getElementById("form-foreigner").checked,
        notes: document.getElementById("form-notes").value
    };

    try {
        if (id === null) {
            await createStudent(student);//новый
        } else {
            await updateStudent(id, student);//существующий
        }

        window.location.href = "index.html"; //перейти на страницу index.html

    } catch (err) {
        //Сервер вернул ошибку — показываем её под нужным полем
        showServerErrors(err);
    }
}

//Получить существующего студента и подставить его данные в поля формы
async function fillForm(id) {
    let student;

    try {
        student = await getStudentById(id);
    } catch (err) {
        alert("Студент не найден");
        window.location.href = "index.html";
        return;
    }

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
    document.getElementById("form-movein").value = student.settlementDate;
    document.getElementById("form-foreigner").checked = student.isForeigner;
    document.getElementById("form-notes").value = student.notes;
}