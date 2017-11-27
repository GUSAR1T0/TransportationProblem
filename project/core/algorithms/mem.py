from project.core.algorithms.tpa import TransportationProblemType
from project.core.data.ps import ProblemStatement


class MinimalElementMethod:
    @staticmethod
    def get_basic_plan(ps: ProblemStatement, costs: list, tpt: int or TransportationProblemType) -> list:
        alpha = ps.productivity[:-1] if tpt == TransportationProblemType.FICTITIOUS_FACTORY else ps.productivity[:]
        beta = ps.consumption[:-1] if tpt == TransportationProblemType.FICTITIOUS_NODE else ps.consumption[:]

        if tpt == TransportationProblemType.BALANCED:
            x = []
            for cost in costs[:]:
                x.append(cost[:])
        elif tpt == TransportationProblemType.FICTITIOUS_FACTORY:
            x = []
            for cost in costs[:-1]:
                x.append(cost[:])
        elif tpt == TransportationProblemType.FICTITIOUS_NODE:
            x = []
            for cost in costs:
                x.append(cost[:-1])
        else:
            raise Exception('Unknown "TransportationProblemType" value')

        for row in x:
            for cell in range(len(row)):
                row[cell] = None

        mask = []
        for i in range(len(alpha)):
            mask_row = []
            for j in range(len(beta)):
                mask_row.append(True)
            mask.append(mask_row)

        while (tpt == TransportationProblemType.BALANCED and sum(alpha) + sum(beta) != 0) or \
                (tpt == TransportationProblemType.FICTITIOUS_FACTORY and sum(alpha) != 0) or \
                (tpt == TransportationProblemType.FICTITIOUS_NODE and sum(beta) != 0):
            minimal = 100000000
            for i in range(len(alpha)):
                for j in range(len(beta)):
                    if (0 < costs[i][j] < minimal) and x[i][j] is None and mask[i][j]:
                        minimal = costs[i][j]

            flag = True
            for i in range(len(alpha)):
                for j in range(len(beta)):
                    if minimal == costs[i][j] and mask[i][j]:
                        loading = min(alpha[i], beta[j])
                        x[i][j] = loading
                        alpha[i] -= loading
                        beta[j] -= loading
                        if alpha[i] == 0:
                            for k in range(len(beta)):
                                if x[i][k] is None:
                                    x[i][k] = 0
                                if mask[i][k]:
                                    mask[i][k] = False
                        if beta[j] == 0:
                            for k in range(len(alpha)):
                                if x[k][j] is None:
                                    x[k][j] = 0
                                if mask[k][j]:
                                    mask[k][j] = False
                        flag = False
                        break
                if flag is False:
                    break

        if tpt == TransportationProblemType.FICTITIOUS_FACTORY:
            row = []
            for i in range(len(beta)):
                row.append(beta[i])
            x.append(row)
        elif tpt == TransportationProblemType.FICTITIOUS_NODE:
            for i in range(len(alpha)):
                x[i].append(alpha[i])

        return x
