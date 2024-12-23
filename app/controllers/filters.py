from app.filters.ComponentsCalculator import ComponentsCalculator
from app.filters.DenormalizedFilters import DenormalizedFilters

filter_validations = {
    'low-pass': {
        'validation': lambda f_pass1, f_stop1, *_: f_pass1 < f_stop1,
        'message': 'O filtro passa-baixas requer que f<sub>pass</sub> seja menor do que f<sub>stop</sub>!'
    },
    'high-pass': {
        'validation': lambda f_pass1, f_stop1, *_: f_stop1 < f_pass1,
        'message': 'O filtro passa-altas requer que f<sub>pass</sub> seja maior do que f<sub>stop</sub>!'
    },
    'band-pass': {
        'validation': lambda f_pass1, f_stop1, f_pass2, f_stop2: f_stop1 < f_pass1 < f_pass2 < f_stop2,
        'message': 'O filtro passa banda requer que f<sub>stop1</sub> < f<sub>pass1</sub> < f<sub>pass2</sub> < f<sub>stop2</sub>!'
    },
    'band-reject': {
        'validation': lambda f_pass1, f_stop1, f_pass2, f_stop2: f_pass1 < f_stop1 < f_stop2 < f_pass2,
        'message': 'O filtro rejeita banda requer que f<sub>pass1</sub> < f<sub>stop1</sub> < f<sub>stop2</sub> < f<sub>pass2</sub>!'
    }
}

def validate_filter(filter_type, a_pass, a_stop, f_pass1, f_stop1, f_pass2=None, f_stop2=None):
    if a_stop >= a_pass:
        return {
            'status': 'warning',
            'title': 'Verifique os ganhos inseridos!',
            'html': 'O valor de a<sub>stop</sub> deve ser menor que a<sub>pass</sub>'
        }

    if filter_type not in filter_validations:
        return {
            'status': 'warning',
            'title': 'Ocorreu um erro inesperado!',
            'html': 'Algo não saiu como esperado. Por favor, tente novamente mais tarde.'
        }

    validation_data = filter_validations[filter_type]
    validation_func = validation_data['validation']
    error_message = validation_data['message']

    if not validation_func(f_pass1, f_stop1, f_pass2, f_stop2):
        return {
            'status': 'warning',
            'title': 'Verifique as frequências inseridas!',
            'html': error_message
        }

    return None

def filter_design(request):
    filter_approx = request.form.get('approx', type=str)
    filter_type = request.form.get('filter', type=str)
    a_pass = request.form.get('a-pass', type=float)
    a_stop = request.form.get('a-stop', type=float)
    f_pass1 = request.form.get('f-pass1', type=float)
    f_stop1 = request.form.get('f-stop1', type=float)
    f_pass2 = request.form.get('f-pass2', type=float)
    f_stop2 = request.form.get('f-stop2', type=float)
    figure_unit = request.form.get('unit', type=str)

    validation_result = validate_filter(filter_type, a_pass, a_stop, f_pass1, f_stop1, f_pass2, f_stop2)

    if validation_result is not None:
        return validation_result

    filter_handle = DenormalizedFilters()
    circuit_handle = ComponentsCalculator()

    if filter_type == 'band-pass' or filter_type == 'band-reject':
        if filter_type == 'band-pass':
            if f_pass1 > f_stop1 and f_stop2 < f_pass2:
                pass
        else:
            pass
    else:
        if filter_type == 'low-pass':
            if filter_approx == 'butterworth':
                filter_handle.create_low_pass_butterworth(a_pass, a_stop, f_pass1, f_stop1)
            elif filter_approx == 'chebyshev':
                filter_handle.create_low_pass_chebyshev(a_pass, a_stop, f_pass1, f_stop1)

            filter_handle.filter_type = 'low-pass'

            circuit_handle.calculate_low_pass_components(filter_handle.d_p)
            circuit_handle.save_circuit()

        elif filter_type == 'high-pass':
            pass

    filter_handle.figure_unit = figure_unit
    filter_handle.image_name = circuit_handle.image_name

    return filter_handle
