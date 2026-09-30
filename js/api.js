

//Адрес сервера
const API_BASE = "http://localhost:8000/api";


//Собирает query-строку из объекта фильтров.
//Пустые значения пропускает.
function buildQueryString(params) {
    const parts = [];

    for (const key in params) {
        const value = params[key];

        if (value !== "" && value !== null && value !== undefined) {
            parts.push(encodeURIComponent(key) + "=" + encodeURIComponent(value));
        }
    }

    if (parts.length === 0) {
        return "";
    }

    return "?" + parts.join("&");
}


//Базовая функция для любого запроса.
//Возвращает распарсенный JSON или бросает ошибку с текстом от сервера.
async function apiRequest(url, options) {
    options = options || {};

    const fetchOptions = {
        method: options.method || "GET",
        headers: { "Content-Type": "application/json" }
    };

    if (options.body !== undefined) {
        fetchOptions.body = options.body;
    }

    const response = await fetch(url, fetchOptions);

    //204 No Content — тело пустое (успешное удаление)
    if (response.status === 204) {
        return null;
    }

    //Пытаемся прочитать JSON
    let data = null;
    try {
        data = await response.json();
    } catch (e) {
        data = null;
    }

    //Сервер ответил ошибкой — бросаем её с понятным текстом
    if (!response.ok) {
        let message = "Ошибка сервера (" + response.status + ")";

        if (data !== null && data.error !== undefined && data.error.message !== undefined) {
            message = data.error.message;
        }

        const err = new Error(message);
        err.status = response.status;
        err.details = (data !== null && data.error !== undefined && data.error.details !== undefined)
            ? data.error.details
            : {};

        throw err;
    }

    return data;
}



//Список студентов (с фильтрами или без)
async function getStudentsFromApi(filters) {
    //Убираем пустые поля из фильтров
    const clean = {};

    for (const key in filters) {
        const v = filters[key];
        if (v !== "" && v !== null && v !== undefined) {
            clean[key] = v;
        }
    }

    const count = Object.keys(clean).length;

    //Мало фильтров — обычный GET с query-параметрами
    if (count <= 2) {
        return apiRequest(API_BASE + "/requests" + buildQueryString(clean));
    }

    //Много фильтров — QUERY с JSON-телом (требование ЛР №2)
    return apiRequest(API_BASE + "/requests", {
        method: "QUERY",
        body: JSON.stringify(clean)
    });
}

//Один студент по id
function getStudentFromApi(id) {
    return apiRequest(API_BASE + "/requests/" + id);
}

//Создание
function createStudentOnApi(studentData) {
    return apiRequest(API_BASE + "/requests", {
        method: "POST",
        body: JSON.stringify(studentData)
    });
}

//Обновление
function updateStudentOnApi(id, studentData) {
    return apiRequest(API_BASE + "/requests/" + id, {
        method: "PATCH",
        body: JSON.stringify(studentData)
    });
}

//Удаление
function deleteStudentOnApi(id) {
    return apiRequest(API_BASE + "/requests/" + id, {
        method: "DELETE"
    });
}