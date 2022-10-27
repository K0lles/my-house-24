function fieldIsValid(element) {
    if (element.tagName === 'SELECT') {
        selectElementValidation(element);
        return null;
    }
    let dict_function_by_type = {
        'text': textTypeValidation,
    }
    dict_function_by_type[$(`#${element.id}`).attr('type')](element);
}

function textTypeValidation(element) {
    if (element.value !== '') {
        element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
        return null;
    }
    else if (element.value === '') {
        if (!($(`#${element.id}-errors`).text()).includes('Поле не може бути пустим')) {
            $(`#${element.id}-errors`).text('Поле не може бути пустим');
            element.style = 'border: 1px solid red';
            return null;
        }

    }

}

function selectElementValidation(element) {
    if (!$(`#${element.id} option:selected`).attr('value')) {
        if (!$(`${element.id}-errors`).text().includes('Виберіть од. вим.')) {
            $(`#${element.id}-errors`).text('Виберіть од. вим.');
        }
        element.style = 'border: 1px solid red';
    }
    else {
        element.style = 'border: 1px solid #58c76d';
        $(`#${element.id}-errors`).text('');
    }
    return null;

}
