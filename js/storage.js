//Работа с cookies(помним студентов)

const COOKIE_NAME = "students";

//Прочитать студентов из cookie
function getStudentsFromStorage() {
    const cookies = document.cookie.split("; ");

    for (let i = 0; i < cookies.length; i++) {
        const parts = cookies[i].split("=");

        if (parts[0] === COOKIE_NAME) {
            try {
                const data = decodeURIComponent(parts[1]);
                return JSON.parse(data); //JSON-строку в JavaScript-данные
            } catch (error) {
                console.error("Ошибка чтения cookie:", error);
                return [];
            }
        }
    }

    return [];
}


//Записать студентов в cookie
function saveStudentsToStorage(students) {
    const data = JSON.stringify(students); //преобразуем в строку

    document.cookie =
        COOKIE_NAME + "=" + encodeURIComponent(data) +
        "; path=/; max-age=31536000";
}