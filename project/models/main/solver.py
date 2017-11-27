from django.http import JsonResponse

from project.core.algorithms.tpa import TransportationProblemAlgorithm


def get_solution(request):
    if request.GET:
        try:
            consumption = _get_values(request.GET.getlist('consumption[]'))
            productivity = _get_values(request.GET.getlist('productivity[]'))

            nodes = []
            for node in list(chunks(request.GET.getlist('nodes[]'), len(productivity))):
                nodes.append(_get_values(node))

            cost_one_ton = _get_values(request.GET.getlist('cost_one_ton[]'))
            daily_cost_loading = _get_values(request.GET.getlist('daily_cost_loading[]'))

            results = TransportationProblemAlgorithm.execute(consumption, productivity, nodes, cost_one_ton,
                                                             daily_cost_loading)

            return JsonResponse(data={'is_successful': True, 'results': results})
        except Exception as e:
            return JsonResponse(data={'is_successful': False, 'errmsg': str(e)})


def _get_values(elements: list):
    try:
        elements = _map_list_to_float(elements)
    except ValueError as e:
        raise Exception('Unable to get values from string list: %s' % str(e))

    if _check_positive_number(elements):
        return elements
    else:
        raise Exception('All numbers should be positive or equal 0')


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def _map_list_to_float(elements: list):
    return list(map(lambda x: float(x), elements))


def _check_positive_number(elements: list):
    if len(elements) > 0:
        for element in elements:
            if element < 0:
                return False
        return True
    else:
        return False
