//Отображение на странице

//Показать всех студентов в таблице на index.html
async function showStudentsTable() {
    //Собираем фильтры (если на странице есть панель) — иначе пустой объект
    const filters = readFilters();
    const students = await getAllStudents(filters);

    const tableBody = document.getElementById("student-table-body");
    const emptyState = document.getElementById("empty-state");

    if (tableBody === null) {
        return;
    }

    tableBody.innerHTML = ""; //удаляем старые строки таблицы

    if (students.length === 0) {
        emptyState.style.display = "block"; //показываем сообщение
        showFilterSummary(0);
        return;
    }

    emptyState.style.display = "none"; //скрываем сообщение
    showFilterSummary(students.length); //пишем "Найдено N"

    for (let i = 0; i < students.length; i++) {
        const student = students[i];

        const row = document.createElement("tr");// создаем новый HTML-элемент

        row.innerHTML =
            "<td>" + student.id + "</td>" +
            "<td>" + student.fullName + "</td>" +
            "<td>" + student.group + "</td>" +
            "<td>" + student.isuId + "</td>" +
            "<td>" + student.dormNumber + "</td>" +
            "<td>" + student.roomNumber + "</td>" +
            "<td>" + (student.isForeigner ? "Да" : "Нет") + "</td>" +
            "<td>" +
                "<a href='student.html?id=" + student.id + "' class='btn btn--small'>Посмотреть</a> " +
                "<a href='form.html?id=" + student.id + "' class='btn btn--small'>Изменить</a> " +
                "<button class='btn btn--danger btn--small' onclick='removeStudent(" + student.id + ")'>Удалить</button>" +
            "</td>";

        tableBody.appendChild(row);
    }
}
//Удаление
async function removeStudent(id) {
    const answer = confirm("Удалить этого студента?");

    if (answer === false) {
        return;
    }

    //Ждём, пока сервер удалит, потом обновляем таблицу
    try {
        await deleteStudent(id);
        await showStudentsTable();
    } catch (err) {
        //Сервер вернул ошибку — показываем её
        alert(err.message || "Не удалось удалить");
    }
}
//Показать досье
async function showStudentProfile() {
    const profile = document.getElementById("profile-content");

    if (profile === null) {
        return;
    }

    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    //Студента теперь берём с сервера — ждём ответ
    let student;
    try {
        student = await getStudentById(id);
    } catch (err) {
        profile.innerHTML = "<p>Студент не найден</p>";
        return;
    }

    if (student === null) {
        profile.innerHTML = "<p>Студент не найден</p>";
        return;
    }

    let foreigner;

    if (student.isForeigner === true) {
        foreigner = "Да";
    } else {
        foreigner = "Нет";
    }

    profile.innerHTML =
        "<p><strong>ФИО:</strong> " + student.fullName + "</p>" +
        "<p><strong>Группа:</strong> " + student.group + "</p>" +
        "<p><strong>ИСУ ID:</strong> " + student.isuId + "</p>" +
        "<p><strong>Общежитие:</strong> " + student.dormNumber + "</p>" +
        "<p><strong>Комната:</strong> " + student.roomNumber + "</p>" +
        "<p><strong>Дата заселения:</strong> " + student.settlementDate + "</p>" +
        "<p><strong>Иностранец:</strong> " + foreigner + "</p>" +
        "<p><strong>Заметки:</strong> " + student.notes + "</p>";
}



//Собрать значения фильтров с панели
function readFilters() {
    function val(id) {
        const el = document.getElementById(id);
        return el ? el.value.trim() : "";
    }

    return {
        group:          val("filter-group").toUpperCase(),
        dormitory:      val("filter-dorm"),
        fullName:       val("filter-name"),
        isuId:          val("filter-isu"),
        roomNumber:     val("filter-room"),
        settlementDate: val("filter-date"),
        isForeigner:    val("filter-foreigner")
    };
}

//Показать "Найдено N студентов" под панелью
function showFilterSummary(count) {
    const el = document.getElementById("filters-summary");
    if (el === null) return;

    if (count === 0) {
        el.textContent = "Ничего не найдено";
    } else if (count === 1) {
        el.textContent = "Найден 1 студент";
    } else {
        el.textContent = "Найдено студентов: " + count;
    }
}

//Сбросить все поля фильтров
function clearFilters() {
    const ids = ["filter-group", "filter-dorm", "filter-name", "filter-isu",
                 "filter-room", "filter-date", "filter-foreigner"];

    for (let i = 0; i < ids.length; i++) {
        const el = document.getElementById(ids[i]);
        if (el !== null) el.value = "";
    }

    const summary = document.getElementById("filters-summary");
    if (summary !== null) summary.textContent = "";
}

//Раскрыть/скрыть расширенный блок фильтров
function toggleAdvancedFilters() {
    const block = document.getElementById("filters-advanced");
    const btn = document.getElementById("btn-filter-toggle");
    if (block === null || btn === null) return;

    if (block.hasAttribute("hidden")) {
        block.removeAttribute("hidden");
        btn.textContent = "⚙️ Скрыть фильтр";
    } else {
        block.setAttribute("hidden", "");
        btn.textContent = "⚙️ Расширенный фильтр";
    }
}