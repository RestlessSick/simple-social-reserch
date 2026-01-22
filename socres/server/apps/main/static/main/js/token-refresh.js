const refresh_token = async () => {
    await fetch('/api-auth/token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((response) => {
        if (!response.ok) {
            if (response.status == 404)
                console.error("Ошибка при обновлении токена. Статус: " + response.status);
            throw "Ошибка при обновлении токена.";
        }
        else {
            console.log("Токен обновлён.");
            return;
        }
    });
}

const start_refresh_routine = () => {
    const interval = setInterval(() => {refresh_token()}, 2 * 60 * 1000);
    return () => { clearInterval(interval) };
}