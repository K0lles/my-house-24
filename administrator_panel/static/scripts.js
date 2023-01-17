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
        'password': passwordTypeValidation
    }
    if ($(`#${element.id}`).attr('type') === 'file') return true;
    return dict_function_by_type[$(`#${element.id}`).attr('type')](element);
}

function textTypeValidation(element) {
    if (element.value !== '') {
        $(`#${element.id}`).css('border', '1px solid #58c76d');
        //element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
        return true;
    }
    else if (element.value === '') {
        $(`#${element.id}`).css('border', '1px solid red');
        //element.style = 'border: 1px solid red';
        if (!($(`#${element.id}-errors`).text()).includes('Поле не може бути пустим')) {
            $(`#${element.id}-errors`).text('Поле не може бути пустим');
            return false;
        }

    }
}

function selectElementValidation(element) {
    if (!$(`#${element.id} option:selected`).attr('value') || $(`#${element.id} option:selected`).attr('value') === 'none') {
        if (!$(`${element.id}-errors`).text().includes('Виберіть елемент') || !$(`${element.id}-errors`).text().includes('Виберіть...')) {
            $(`#${element.id}-errors`).text('Виберіть елемент');
        }
        $(`#${element.id}`).css('border', '1px solid red');
        //element.style = 'border: 1px solid red';
        return false;
    }
    else {
        $(`#${element.id}`).css('border', '1px solid #58c76d');
        //element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
        return true;
    }
}

function numberTypeValidation(element) {

    if (element.value !== '' && element.value > 0.00) {
        $(`#${element.id}`).css('border', '1px solid #58c76d');
        //element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
        return true;
    }
    else if (element.value === '') {
        $(`#${element.id}`).css('border', '1px solid red');
        //element.style = 'border: 1px solid red';
        if (!($(`#${element.id}-errors`).text()).includes('Поле не може бути пустим')) {
            $(`#${element.id}-errors`).text('Поле не може бути пустим');
            return false;
        }
    }
    else if (element.value <= 0.00) {
        $(`#${element.id}`).css('border', '1px solid red');
        //element.style = 'border: 1px solid red';
        if (!($(`#${element.id}-errors`).text()).includes('Цифра у полі не може бути меншою 0')) {
            $(`#${element.id}-errors`).text('Цифра у полі не може бути меншою 0');
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
        $(`#${element.id}`).css('border', '1px solid red');
        //element.style = 'border: 1px solid red';
        return false;
    }

    else {
        $(`#${element.id}`).css('border', '1px solid #58c76d');
        //element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
        return true;
    }

}

function passwordTypeValidation(element) {
    if (element.id === 'id_repeat-password') {
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
            $(`#${element.id}`).css('border', '1px solid #58c76d');
            //element.style = 'border: 1px solid #58c76d';
            $(`#${element.id}-errors`).text('');
            return true;
        } else if (element.value === '') {
            if (!($(`#${element.id}-errors`).text()).includes('Поле не може бути пустим')) {
                $(`#${element.id}-errors`).text('Поле не може бути пустим');
                $(`#${element.id}`).css('border', '1px solid red');
                //element.style = 'border: 1px solid red';
            }
            return false;
        } else if ($('#id_repeat-password').val() !== element.value) {
            $(`#${element.id}`).css('border', '1px solid red');
            //element.style = 'border: 1px solid red';
            if (!($(`#${element.id}-errors`).text()).includes('Паролі повинні співпадати')) {
                $(`#${element.id}-errors`).text('Паролі повинні співпадати');
            }
            return false;
        }
    }
    return true;
}

function validatePasswordUpdate(element) {
    if (element.id === 'id_repeat-password') {
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
                $(`#${element.id}`).css('border', '1px solid red');
                //element.style = 'border: 1px solid red';
            }
            return false;
        }
    }
    $('#id_password').css('border', '1px solid #58c76d');
    $(`#id_password-errors`).text('');
    return true;
}

function alwaysIsValid(element) {
    $(`#${element.id}`).css('border', '1px solid #58c76d');
    //element.style = 'border: 1px solid #58c76d';
}


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


let characters ='0123456789';

function generateNumber() {
    let result = '';
    const charactersLength = characters.length;
    for ( let i = 0; i < 8; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    return result;
}

function generatePassword() {
        let randomstring = Math.random().toString(36).slice(-8);
        $('#id_password').val(randomstring);
        $('#id_repeat-password').val(randomstring);
    }

function showHidePassword() {
    let type = $('#id_password').attr('type');
    if (type === 'password') {
        $('#id_password').attr('type', 'text');
        $('#id_repeat-password').attr('type', 'text');
        $('.fa-eye').attr('class', 'fa fa-eye-slash');
    }
    else {
        $('#id_password').attr('type', 'password');
        $('#id_repeat-password').attr('type', 'password');
        $('.fa-eye-slash').attr('class', 'fa fa-eye');
    }
}
