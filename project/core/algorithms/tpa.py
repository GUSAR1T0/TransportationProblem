from copy import deepcopy

from project.core.algorithms.pm import PotentialMethod
from project.core.data.ps import ProblemStatement


class TransportationProblemType:
    BALANCED = 0
    FICTITIOUS_FACTORY = 1
    FICTITIOUS_NODE = 2


class TransportationProblemAlgorithm:
    @staticmethod
    def execute(consumption, productivity, nodes, cost_one_ton, daily_cost_loading) -> dict:
        from project.core import utils
        from project.core.algorithms.mem import MinimalElementMethod

        results = {}

        ps = ProblemStatement(consumption, productivity, nodes, cost_one_ton, daily_cost_loading)
        results['problem_statement'] = utils.get_problem_statement(ps)
        ps_copy = deepcopy(ps)

        costs, tpt, diff = TransportationProblemAlgorithm.__prepare(ps, ps.get_costs())
        x = MinimalElementMethod.get_basic_plan(ps, costs, tpt)
        results['basic_diff'] = utils.get_basic_diff(ps_copy, diff)
        results['minimal_element_method'] = utils.get_basic_plan(x, costs, tpt)

        expected_count = len(ps.consumption) + len(ps.productivity) - 1
        actual_count = 0
        for row in x:
            actual_count += len(list(filter(lambda element: element != .0, row)))
        results['non-degenerated_values'] = utils.get_non_degenerated_values(actual_count, ps)

        results['step_table'] = []
        results['pseudos'] = []
        results['diffs'] = []
        results['potential_method'] = []
        results['theta'] = []
        results['table_after'] = []

        if actual_count == expected_count:
            results['non-degenerated'] = utils.get_non_degenerated_status(True)
            while True:
                alpha, beta, pseudos, diffs, flag = TransportationProblemAlgorithm.__get_diffs_and_status(ps, x, costs)
                results['step_table'].append(utils.get_step_table(alpha, beta, x, costs))
                results['pseudos'].append(utils.get_pseudos(alpha, beta, pseudos))
                results['diffs'].append(utils.get_diffs(costs, pseudos, diffs))

                if flag:
                    break
                else:
                    before_x = deepcopy(x)
                    pm_results = PotentialMethod.perform_iteration(x, diffs)
                    results['potential_method'].append(utils.get_potential_method_values(
                        before_x, costs, pm_results))
                    results['theta'].append(utils.get_theta(before_x, pm_results))
                    results['table_after'].append(utils.get_table_after_pm(x, costs, pm_results))
        else:
            results['non-degenerated'] = utils.get_non_degenerated_status(False)
            possible_non_degenerated_plans = []
            TransportationProblemAlgorithm.__do_possible_non_degenerated_plans(x, expected_count - actual_count, 0, 0,
                                                                               possible_non_degenerated_plans)
            results['errors'] = []

            for possible_non_degenerated_plan in possible_non_degenerated_plans:
                try:
                    while True:
                        alpha, beta, pseudos, diffs, flag = TransportationProblemAlgorithm.__get_diffs_and_status(
                            ps, possible_non_degenerated_plan, costs)
                        results['step_table'].append(utils.get_step_table(alpha, beta, possible_non_degenerated_plan,
                                                                          costs))
                        results['pseudos'].append(utils.get_pseudos(alpha, beta, pseudos))
                        results['diffs'].append(utils.get_diffs(costs, pseudos, diffs))

                        if flag:
                            break
                        else:
                            before_x = deepcopy(possible_non_degenerated_plan)
                            pm_results = PotentialMethod.perform_iteration(possible_non_degenerated_plan, diffs)
                            results['potential_method'].append(utils.get_potential_method_values(
                                before_x, costs, pm_results))
                            results['theta'].append(utils.get_theta(before_x, pm_results))
                            results['table_after'].append(utils.get_table_after_pm(
                                possible_non_degenerated_plan, costs, pm_results))

                    x = possible_non_degenerated_plan
                    break
                except Exception as e:
                    results['errors'].append((deepcopy(possible_non_degenerated_plan), str(e)))

        rows = len(x) - 1 if tpt == TransportationProblemType.FICTITIOUS_FACTORY else len(x)
        cols = len(x[0]) - 1 if tpt == TransportationProblemType.FICTITIOUS_NODE else len(x[0])
        objective_function_value = .0
        for i in range(rows):
            for j in range(cols):
                if x[i][j] > .0:
                    objective_function_value += round(costs[i][j] * x[i][j] + ps.daily_cost_loading[i], 2)

        results['final'] = utils.get_final(x, costs, rows, cols)
        results['objective_function_value'] = utils.get_objective_function_value(objective_function_value)

        return results

    @staticmethod
    def __prepare(ps: ProblemStatement, costs: list) -> (list, int or TransportationProblemType):
        a = sum(ps.productivity)
        b = sum(ps.consumption)
        diff = round(a - b, 2)

        if diff < .0:
            ps.productivity.append(abs(diff))
            nullable = []
            for i in range(len(ps.consumption)):
                nullable.append(.0)
            costs.append(nullable)
            tpt = TransportationProblemType.FICTITIOUS_FACTORY
        elif diff > .0:
            ps.consumption.append(diff)
            for cost in costs:
                cost.append(.0)
            tpt = TransportationProblemType.FICTITIOUS_NODE
        else:
            tpt = TransportationProblemType.BALANCED

        return costs, tpt, diff

    @staticmethod
    def __do_possible_non_degenerated_plans(x: list, epsilons: int, prev_i: int, prev_j: int, l: list) -> None:
        if epsilons > 0:
            for i in range(prev_i, len(x)):
                for j in range(prev_j, len(x[i])):
                    if x[i][j] == .0:
                        x[i][j] = .000000001
                        TransportationProblemAlgorithm.__do_possible_non_degenerated_plans(x, epsilons - 1, i, j, l)
                        x[i][j] = .0
        else:
            l.append(list(map(list, x)))

    @staticmethod
    def __get_diffs_and_status(ps: ProblemStatement, x: list, costs: list) -> tuple:
        alpha = [.0, ]
        for i in range(len(ps.productivity) - 1):
            alpha.append(None)
        beta = []
        for i in range(len(ps.consumption)):
            beta.append(None)

        while alpha.count(None) != .0 or beta.count(None) != .0:
            alpha_before = alpha[:]
            beta_before = beta[:]

            for i in range(len(alpha)):
                for j in range(len(beta)):
                    if x[i][j] != .0 and (alpha[i] is not None or beta[j] is not None):
                        if alpha[i] is not None:
                            beta[j] = round(costs[i][j] - alpha[i], 2)
                        elif beta[j] is not None:
                            alpha[i] = round(costs[i][j] - beta[j], 2)

            is_changed = TransportationProblemAlgorithm.__check_changes(alpha_before, alpha, beta_before, beta)
            if not is_changed:
                raise Exception('Table is not applicable for calculations', x)

        pseudos = []
        for i in range(len(alpha)):
            pseudo_row = []
            for j in range(len(beta)):
                pseudo_row.append(round(alpha[i] + beta[j], 2))
            pseudos.append(pseudo_row)

        status = True
        diffs = []
        for i in range(len(alpha)):
            diffs_row = []
            for j in range(len(beta)):
                diffs_row.append(round(costs[i][j] - pseudos[i][j], 2))
                if diffs_row[-1] < .0:
                    status = False
            diffs.append(diffs_row)

        return alpha, beta, pseudos, diffs, status

    @staticmethod
    def __check_changes(alpha_before: list, alpha: list, beta_before: list, beta: list) -> bool:
        for i in range(len(alpha)):
            if alpha[i] != alpha_before[i]:
                return True

        for j in range(len(beta)):
            if beta[j] != beta_before[j]:
                return True

        return False
