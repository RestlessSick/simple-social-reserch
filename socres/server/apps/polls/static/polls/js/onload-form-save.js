document.addEventListener('DOMContentLoaded', () => {
    let inputs = document.querySelectorAll('textarea, input');
    console.log(inputs)
    inputs.forEach((e) => {
        if (e.name != 'csrfmiddlewaretoken' && e.type != 'submit') {
            if (e.name.split('-')[0] == 'text' || e.name.split('-')[0] == 'number')
            {   
                if (e.value === '')
                    e.value = window.sessionStorage.getItem(e.name)
                e.addEventListener('input', () => {
                    window.sessionStorage.setItem(e.name, e.value)
                });
                
            }
        }
    });

});