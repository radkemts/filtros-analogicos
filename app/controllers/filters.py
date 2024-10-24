from app.filters.ComponentsCalculator import ComponentsCalculator
from app.filters.DenormalizedFilters import DenormalizedFilters

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

    filter_handle = DenormalizedFilters()

    if f_pass2 is not None and f_stop2 is not None:
        if f_pass1 > f_stop1 and f_stop2 < f_pass2:
            # Band Pass
            pass
        else:
            # Band Reject
            pass
    else:
        if f_pass1 < f_stop1:
            # Low Pass

            if filter_approx == 'butterworth':
                filter_handle.create_low_pass_butterworth(a_pass, a_stop, f_pass1, f_stop1)
            elif filter_approx == 'chebyshev':
                filter_handle.create_low_pass_chebyshev(a_pass, a_stop, f_pass1, f_stop1)

            filter_handle.filter_type = 'low-pass'

            circuit_handle = ComponentsCalculator()
            circuit_handle.calculate_low_pass_components(filter_handle.d_p)
            circuit_handle.save_circuit()

        else:
            # High Pass
            pass

    filter_handle.figure_unit = figure_unit

    return filter_handle