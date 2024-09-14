$(document).ready(function() {
    $('.div-input-text input[type="text"]').on('input', function() {
        let value = $(this).val();
        let newValue = '';

        if (value.length > 0 && value[0] === '-') {
            newValue = '-';
            value = value.slice(1);
        }

        let hasDot = false;
        for (let char of value) {
            if (char === '.' && !hasDot) {
                newValue += '.';
                hasDot = true;
            } else if (!isNaN(char) && char !== ' ') {
                newValue += char;
            }
        }

        $(this).val(newValue);
    });
});