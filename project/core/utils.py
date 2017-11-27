from project.core.algorithms.tpa import TransportationProblemType
from project.core.data.ps import ProblemStatement


def get_problem_statement(ps: ProblemStatement) -> str:
    string = '\\begin{gathered}X(i,j) - \\text{масса песка в тоннах, перевозимая от фабрики к узлу.}\\\\\\\\'

    string += 'X(i,j) \ge 0, i = \overline{1,%d}, j = \overline{1,%d}\\\\\\\\' % \
              (len(ps.productivity), len(ps.consumption))

    for i, element in enumerate(ps.consumption):
        equation = []
        for j in range(len(ps.productivity)):
            equation.append('X(%d,%d)' % (j + 1, i + 1))
        string += '%s = %s\\\\' % (' + '.join(equation), element)

    for i, element in enumerate(ps.productivity):
        equation = []
        for j in range(len(ps.consumption)):
            equation.append('X(%d,%d)' % (i + 1, j + 1))
        string += '%s = %s\\\\' % (' + '.join(equation), element)

    string += '\\\\'

    string += 'Y(i,j) = \\begin{cases}0 &\\text{если } X(i,j) = 0, i = \overline{1,%d}, j = \overline{1,%d}\\\\' \
              '1 &\\text{если } X(i,j) > 0, i = \overline{1,%d}, j = \overline{1,%d}\end{cases}\\\\' % \
              (len(ps.productivity), len(ps.consumption), len(ps.productivity), len(ps.consumption))

    string += '\\\\'

    objective_function = []
    for i in range(len(ps.productivity)):
        for j in range(len(ps.consumption)):
            objective_function.append('(%s + %s) * X(%d,%d) + %s * Y(%d,%d)' % (ps.nodes[j][i],
                                                                                ps.cost_one_ton[i],
                                                                                i + 1, j + 1,
                                                                                ps.daily_cost_loading[i],
                                                                                i + 1, j + 1))
    string += 'F = %s\\\\' % (' + \\\\'.join(objective_function))
    string += 'F \\to min'

    string += '\end{gathered}'

    return string


def get_basic_diff(ps: ProblemStatement, diff: float):
    string = '\\begin{gathered}\displaystyle\sum_{i=1}^%d\\alpha(i) - ' \
            '\displaystyle\sum_{j=1}^%d\\beta(j) = %f\end{gathered}' % \
            (len(ps.consumption), len(ps.productivity), diff)
    return string


def get_basic_plan(x: list, costs: list, tpt: (int or TransportationProblemType)) -> str:
    if tpt == TransportationProblemType.BALANCED:
        string_type = 'сбалансированной'
    elif tpt == TransportationProblemType.FICTITIOUS_FACTORY:
        string_type = 'не сбалансированной (с фиктивной фабрикой)'
    elif tpt == TransportationProblemType.FICTITIOUS_NODE:
        string_type = 'не сбалансированной (с фиктивным узлом)'
    else:
        string_type = 'с неизвестным типом'
    string = 'Задача является <strong>%s</strong>.<br><br>' % string_type

    string += '<table class="table table-hover" width="100%">'
    for i in range(len(x)):
        string += '<tr>'
        for j in range(len(x[i])):
            string += '<td>' + str(x[i][j]) + ' | ' + str(costs[i][j]) + '</td>'
        string += '</tr>'
    string += '</table>'

    return string


def get_non_degenerated_values(actual_count: int, ps: ProblemStatement) -> str:
    string = '\\begin{gathered}m + n - 1 = %d + %d - 1 = ' % (len(ps.consumption), len(ps.productivity)) + \
             '%s\\\\' % (len(ps.consumption) + len(ps.productivity) - 1) + \
             'non-zeros = ' + str(actual_count) + '\end{gathered}'
    return string


def get_non_degenerated_status(status: bool) -> str:
    return 'Задача является <strong>%s</strong>.' % ('невырожденной' if status else 'вырожденной')


def get_step_table(alpha: list, beta: list, x: list, costs: list) -> str:
    string = '<br><table class="table table-hover" width="100%">'
    string += '<tr>' + '<th></th>'
    for j in range(len(beta)):
        string += '<th>b = ' + str(beta[j]) + '</th>'

    for i in range(len(alpha)):
        string += '<tr>' + '<th>a = ' + str(alpha[i]) + '</th>'
        for j in range(len(beta)):
            string += '<td>' + str(x[i][j]) + ' | ' + str(costs[i][j]) + '</td>'
        string += '</tr>'
    string += '</table><br>'

    return string


def get_pseudos(alpha: list, beta: list, pseudos: list) -> str:
    string = '\\begin{gathered}'

    for i in range(len(pseudos)):
        for j in range(len(pseudos[i])):
            string += '\widetilde{C}(%d,%d) = %s + %s = %s\\\\' % (i + 1, j + 1, alpha[i], beta[j], pseudos[i][j])

    string += '\end{gathered}'
    return string


def get_diffs(costs: list, pseudos: list, diffs: list) -> str:
    string = '\\begin{gathered}'

    for i in range(len(diffs)):
        for j in range(len(diffs[i])):
            string += '\Delta C(%d,%d) = %s - %s = %s\\\\' % (i + 1, j + 1, costs[i][j], pseudos[i][j], diffs[i][j])

    string += '\end{gathered}'
    return string


def get_potential_method_values(x: list, costs: list, results: dict) -> str:
    string = '<br><table class="table table-hover" width="100%">'
    for i in range(len(x)):
        string += '<tr>'
        for j in range(len(x[i])):
            if results['path'].count((i, j)) > 0:
                if results['path'][0] == (i, j):
                    string += '<td style="background-color: rgba(0, 255, 0, 0.25)">' + \
                              str(x[i][j]) + ' | ' + str(costs[i][j]) + '</td>'
                elif results['corners'].count((i, j)) > 0:
                    string += '<td style="background-color: rgba(0, 0, 255, 0.25)">' + \
                              str(x[i][j]) + ' | ' + str(costs[i][j]) + '</td>'
                else:
                    string += '<td style="background-color: rgba(255, 0, 0, 0.25)">' + \
                              str(x[i][j]) + ' | ' + str(costs[i][j]) + '</td>'
            else:
                string += '<td>' + \
                          str(x[i][j]) + ' | ' + str(costs[i][j]) + '</td>'
        string += '</tr>'
    string += '</table><br>'

    return string


def get_theta(x: list, results: dict) -> str:
    string = '\\begin{gathered}'

    for element in results['negative_corners']:
        string += 'X(%d,%d) = %s\\\\' % (element[0] + 1, element[1] + 1, x[element[0]][element[1]])

    string += '\Theta = \min ('
    for element in results['negative_corners']:
        string += 'X(%d,%d)' % (element[0] + 1, element[1] + 1)
        if element != results['negative_corners'][-1]:
            string += ', '
    string += ') = %s' % results['theta']

    string += '\end{gathered}'
    return string


def get_table_after_pm(x: list, costs: list, results: dict) -> str:
    string = '<table class="table table-hover" width="100%">'
    for i in range(len(x)):
        string += '<tr>'
        for j in range(len(x[i])):
            if results['corners'].count((i, j)) > 0:
                string += '<td style="background-color: rgba(0, 255, 0, 0.25)">' + \
                          str(x[i][j]) + ' | ' + str(costs[i][j]) + '</td>'
            elif results['path'].count((i, j)) > 0:
                string += '<td style="background-color: rgba(255, 0, 0, 0.25)">' + \
                          str(x[i][j]) + ' | ' + str(costs[i][j]) + '</td>'
            else:
                string += '<td>' + str(x[i][j]) + ' | ' + str(costs[i][j]) + '</td>'
        string += '</tr>'
    string += '</table>'

    return string


def get_final(x: list, costs: list, rows: int, cols: int) -> str:
    string = '<table class="table table-hover" width="100%">'
    for i in range(rows):
        string += '<tr>'
        for j in range(cols):
            if round(x[i][j], 2) != .0:
                string += '<td style="background-color: rgba(125, 125, 125, 0.25)">' + str(round(x[i][j], 2)) + ' | ' \
                          + str(round(costs[i][j], 2)) + '</td>'
            else:
                string += '<td>' + str(round(x[i][j], 2)) + ' | ' + str(round(costs[i][j], 2)) + '</td>'
        string += '</tr>'
    string += '</table>'

    return string


def get_objective_function_value(value: float) -> str:
    return '\\begin{gathered}F = ' + str(value) + '\\text{ (руб.)}\end{gathered}'
