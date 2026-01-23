let sleep = async (ms) => {
    return new Promise(resolve => { setTimeout(resolve, ms) });
}

let get_cookie = async (name) => {
    let cookies = cookieStore.get(name);
    cookies.then((value) => console.log(value));

    return 0;
}

window.addEventListener('DOMContentLoaded', async () => {
    try {
        await refresh_token();
        stop_routine = start_refresh_routine();
        document.querySelectorAll('#register-button, #login-button').forEach(element => {
            element.classList.add('hidden');
        });
        document.getElementById('profile').classList.remove('hidden');
    }
    catch (error) {
        console.log(error);
    }
    await sleep(500);
    document.querySelector('.fade-out').classList.add('hidden');
})