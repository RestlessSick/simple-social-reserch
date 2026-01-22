document.getElementById('create-form').addEventListener('submit', (event) => {
    event.preventDefault();
    let form = document.getElementById('create-form'); 
    let result = {};
    result['Poll'] = {
        'theme': document.getElementById('poll-theme').value,
        'description': document.getElementById('poll-descr').value,
        'questions': new Array(),
    };

    for (let i = 1; i <= document.querySelectorAll('.question').length; i++) {
        let question = document.getElementById(String(i));
        let question_dict = {
            'question': question.querySelector('#question-' + i + '-question').value,
            'field_type': question.querySelector('#question-' + i + '-field_type').value,
            'fields': new Array(),
        };

        if (question_dict['field_type'] == 'RadioField') {
            question_dict['choices'] = new Array();
            for (let j = 1; j <= question.querySelectorAll('.choice').length; j++) {
                question_dict['choices'].push({ 'text': question.querySelector('#question-' + i + '-choice-' + j).value });
        }
        }

        for (let j = 1; j <= question.querySelectorAll('.field').length; j++) {
            question_dict['fields'].push({ 'note': question.querySelector('#question-' + i + '-field-' + j).value });
        }

        result['Poll']['questions'].push(question_dict);
    }

    fetch(form.action, {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(result),
    }).then(async response => {
        if (!response.ok) {
            console.error(('Ошибка при создании опросника. '));
            await message('Ошибка при создании опросника. Проверьте введённые данные и повторите попытку.')
        }
        else {
            await message('Опросник успешно создан. Перенаправляем вас.')
            window.location.href = '/';
        }
    });

    console.log(result);

});