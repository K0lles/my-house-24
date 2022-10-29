function fieldIsValid(element) {
    if (element.tagName === 'SELECT') {
        return selectElementValidation(element);
    }
    if (element.tagName === 'TEXTAREA') {
        return textTypeValidation(element);
    }
    let dict_function_by_type = {
        'text': textTypeValidation,
        'number': numberTypeValidation,
        'email': emailTypeValidation,
        'password': passwordTypeValidation,
    }
    if ($(`#${element.id}`).attr('type') === 'file') return true;
    return dict_function_by_type[$(`#${element.id}`).attr('type')](element);
}

function textTypeValidation(element) {
    if (element.value !== '') {
        element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
        return true;
    }
    else if (element.value === '') {
        if (!($(`#${element.id}-errors`).text()).includes('Поле не може бути пустим')) {
            $(`#${element.id}-errors`).text('Поле не може бути пустим');
            element.style = 'border: 1px solid red';
            return false;
        }

    }
}

function selectElementValidation(element) {
    if (!$(`#${element.id} option:selected`).attr('value') || $(`#${element.id} option:selected`).attr('value') === 'none') {
        if (!$(`${element.id}-errors`).text().includes('Виберіть елемент')) {
            $(`#${element.id}-errors`).text('Виберіть елемент');
        }
        element.style = 'border: 1px solid red';
        return false;
    }
    else {
        element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
        return true;
    }
}

function numberTypeValidation(element) {

    if (element.value !== '' && element.value > 0.00) {
        element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
        return true;
    }
    else if (element.value === '') {
        if (!($(`#${element.id}-errors`).text()).includes('Поле не може бути пустим')) {
            $(`#${element.id}-errors`).text('Поле не може бути пустим');
            element.style = 'border: 1px solid red';
            return false;
        }
    }
    else if (element.value <= 0.00) {
        if (!($(`#${element.id}-errors`).text()).includes('Ціна не може бути меншою 0')) {
            $(`#${element.id}-errors`).text('Ціна не може бути меншою 0');
            element.style = 'border: 1px solid red';
            return false;
        }
    }

}

function emailTypeValidation(element) {
    let emailValid;
    emailValid = textTypeValidation(element)
    if (!emailValid) return emailValid;
    if (!(element.value).match(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
        $(`#${element.id}-errors`).text('Неправильно введений email');
        element.style = 'border: 1px solid red';
        return false;
    }

    else {
        element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
        return true;
    }

}

function passwordTypeValidation(element) {
    if (element.id === 'id_repeat-password') {
        console.log('we are here')
        if ($('#id_password').val() !== element.value) {
            if (!($(`#id_password-errors`).text()).includes('Паролі повинні співпадати')) {
                $(`#id_password-errors`).text('Паролі повинні співпадати');
                $('#id_password').css('border', '1px solid red');
            }
            return false;
        }
        else if ($('#id_password').val() === element.value && element.value !== '') {
            $('#id_password').css('border', '1px solid #58c76d');
            $(`#id_password-errors`).text('');
            return true;
        }
    }
    else {
        if (element.value !== '' && $('id_repeat-password').val() !== '' && $('#id_repeat-password').val() === element.value) {
            element.style = 'border: 1px solid #58c76d';
            $(`#${element.id}-errors`).text('');
            return true;
        } else if (element.value === '') {
            if (!($(`#${element.id}-errors`).text()).includes('Поле не може бути пустим')) {
                $(`#${element.id}-errors`).text('Поле не може бути пустим');
                element.style = 'border: 1px solid red';
            }
            return false;
        } else if ($('#id_repeat-password').val() !== element.value) {
            if (!($(`#${element.id}-errors`).text()).includes('Паролі повинні співпадати')) {
                $(`#${element.id}-errors`).text('Паролі повинні співпадати');
                element.style = 'border: 1px solid red';
            }
            return false;
        }
    }
    return true;
}

function validatePasswordUpdate(element) {
    if (element.id === 'id_repeat-password') {
        console.log('we are here')
        if ($('#id_password').val() !== element.value) {
            if (!($(`#id_password-errors`).text()).includes('Паролі повинні співпадати')) {
                $(`#id_password-errors`).text('Паролі повинні співпадати');
                $('#id_password').css('border', '1px solid red');
            }
            return false;
        }
    }
    else {
        if ($('#id_repeat-password').val() !== element.value) {
            if (!($(`#${element.id}-errors`).text()).includes('Паролі повинні співпадати')) {
                $(`#${element.id}-errors`).text('Паролі повинні співпадати');
                element.style = 'border: 1px solid red';
            }
            return false;
        }
    }
    $('#id_password').css('border', '1px solid #58c76d');
    $(`#id_password-errors`).text('');
    return true;
}

/*function formIsValid() {
    function formIsValid(e) {
        e.preventDefault();
        let isValidName = true;
        let isValidSelect = true;

        $(`#article-payment-form`).find(`input[id$='_name']`).each(function() {
            if (!fieldIsValid(this)) {
                isValidName = false;
            }
        });

        $(`#article-payment-form`).find(`select[id$='_type']`).each(function() {
            if (!fieldIsValid(this)) {
                isValidSelect = false;
            }
        });

        if (isValidName && isValidSelect) {
            $(`#article-payment-form`).submit();
            return true;
        }
        else {
            return false;
        }
    }
}*/

$('tr[data-href]').on('click', function() {
    document.location = $(this).data('href');
});


function loadFile(event, id) {
    event.preventDefault();

    let image = $(`#${id}-display`);
    image.attr('src', URL.createObjectURL(event.target.files[0]));
    image.onload = function() {
        URL.revokeObjectURL(image.src);
    };
}
