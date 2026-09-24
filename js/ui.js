//Отображение на странице

//Показать всех студентов в таблице на index.html
function showStudentsTable() {
    const students = getAllStudents();

    const tableBody = document.getElementById("student-table-body");
    const emptyState = document.getElementById("empty-state");

    if (tableBody === null) {
        return;
    }

    tableBody.innerHTML = ""; //удаляем старые строки таблицы

    if (students.length === 0) {
        emptyState.style.display = "block"; //показываем сообщение
        return;
    }

    emptyState.style.display = "none"; //скрываем сообщение

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
function removeStudent(id) {
    const answer = confirm("Удалить этого студента?");

    if (answer === false) {
        return;
    }

    deleteStudent(id);
    showStudentsTable();
}
//Показать досье
function showStudentProfile() {
    const profile = document.getElementById("profile-content");

    if (profile === null) {
        return;
    }

    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    const student = getStudentById(id);

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
        "<p><strong>Дата заселения:</strong> " + student.moveInDate + "</p>" +
        "<p><strong>Иностранец:</strong> " + foreigner + "</p>" +
        "<p><strong>Заметки:</strong> " + student.notes + "</p>";
}