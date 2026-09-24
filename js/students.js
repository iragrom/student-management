//CRUD студентов

//Получить всех студентов
function getAllStudents() {
    return getStudentsFromStorage();
}

//Получить студента по id
function getStudentById(id) {
    const students = getStudentsFromStorage();

    for (let i = 0; i < students.length; i++) {
        if (students[i].id === Number(id)) {
            return students[i];
        }
    }

    return null;
}

//ID
function getNewId(students) {
    let maxId = 0;

    for (let i = 0; i < students.length; i++) {
        if (students[i].id > maxId) {
            maxId = students[i].id;
        }
    }

    return maxId + 1;
}

//Возвращаем созданного студента
function createStudent(studentData) {
    const students = getStudentsFromStorage();

    studentData.id = getNewId(students);

    students.push(studentData);//добавляем в конец массива

    saveStudentsToStorage(students);

    return studentData;
}

//Заменить данные студента
function updateStudent(id, studentData) {
    const students = getStudentsFromStorage();

    for (let i = 0; i < students.length; i++) {

        if (students[i].id === Number(id)) {

            studentData.id = students[i].id;

            students[i] = studentData;

            saveStudentsToStorage(students);

            return true;
        }
    }

    return false;
}

//Удаление
function deleteStudent(id) {
    const students = getStudentsFromStorage();

    for (let i = 0; i < students.length; i++) {

        if (students[i].id === Number(id)) {

            students.splice(i, 1);

            saveStudentsToStorage(students);

            return true;
        }
    }

    return false;
}