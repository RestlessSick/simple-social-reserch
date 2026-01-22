const message = async (msg) => {
    hint = document.getElementById('floating-hint');
    hint.innerText = msg;
    hint.classList.toggle('hidden');
    await(sleep(2000));
    hint.classList.toggle('hidden');
};