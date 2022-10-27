function fieldIsValid(element) {
    if (element.tagName === 'SELECT') {
        return selectElementValidation(element);
    }
    if (element.tagName === 'TEXTAREA') {
        return textTypeValidation(element);
    }
    let dict_function_by_type = {
        'text': textTypeValidation,
        'number': numberTypeValidation
    }
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
        if (!$(`${element.id}-errors`).text().includes('Виберіть од. вим.')) {
            $(`#${element.id}-errors`).text('Виберіть од. вим.');
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
