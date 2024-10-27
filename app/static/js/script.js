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

    $('.formulario').on('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(this);
        const url = $(this).attr('action');

        const a_pass = parseFloat(formData.get('a-pass'));
        const a_stop = parseFloat(formData.get('a-stop'));
        const f_pass1 = parseFloat(formData.get('f-pass1'));
        const f_stop1 = parseFloat(formData.get('f-stop1'));
        const f_pass2 = parseFloat(formData.get('f-pass2'));
        const f_stop2 = parseFloat(formData.get('f-stop2'));
        const filter = formData.get('filter');

        const showAlert = (status, title, message) => {
            Swal.fire({
                icon: status,
                title: title,
                html: message
            });
        };

        if (a_stop >= a_pass) {
            showAlert('warning', 'Verifique os ganhos inseridos!', 'O valor de a<sub>stop</sub> deve ser menor que a<sub>pass</sub>!');
            return;
        }

        const filterValidations = {
            'low-pass': () => f_pass1 >= f_stop1,
            'high-pass': () => f_stop1 >= f_pass1,
            'band-pass': () => (f_stop1 >= f_pass1 || f_pass2 >= f_stop2),
            'band-reject': () => (f_pass1 >= f_stop1 || f_stop2 >= f_pass2)
        };

        const errorMessages = {
            'low-pass': 'O filtro passa-baixas requer que f<sub>pass</sub> seja menor do que f<sub>stop</sub>!',
            'high-pass': 'O filtro passa-altas requer que f<sub>pass</sub> seja maior do que f<sub>stop</sub>!',
            'band-pass': 'O filtro passa banda requer que f<sub>stop1</sub> < f<sub>pass1</sub> < f<sub>pass2</sub> < f<sub>stop2</sub>!',
            'band-reject': 'O filtro rejeita banda requer que f<sub>pass1</sub> < f<sub>stop1</sub> < f<sub>stop2</sub> < f<sub>pass2</sub>!'
        };

        if (filterValidations[filter] && filterValidations[filter]()) {
            showAlert('warning', 'Verifique as frequências inseridas!', errorMessages[filter]);
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if(response.status === 'warning') {
                    showAlert(response.status, response.title, response.message);
                } else {
                    $('#resultado').html(response.template);
                    $('#resultado').each(function() {
                        $(this).find('a').attr('href', function(i, href) {
                            return href.split('?')[0] + '?' + new Date().getTime();
                        });
                        $(this).find('img').attr('src', function(i, src) {
                            return src.split('?')[0] + '?' + new Date().getTime();
                        });
                    });
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                showAlert('error', 'Ocorreu um erro inesperado!', 'Algo não saiu como esperado. Por favor, tente novamente mais tarde.');
            }
        });
    });

    Fancybox.bind('[data-fancybox]', {
        animationEffect: 'fade',
        on: {
            ready: (instance) => {
                const backdrop = document.querySelector('.fancybox__backdrop');
                if (backdrop) {
                    backdrop.style.backgroundColor = '#E0E3DD';
                }
            }
        }
    });

    $('.botao-enviar').on('mousedown touchstart', function() {
        $(this).addClass('botao-pressionado');
    });

    $('.botao-enviar').on('mouseup mouseleave touchend', function() {
        $(this).removeClass('botao-pressionado');
    });

});