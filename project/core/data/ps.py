class ProblemStatement:
    def __init__(self, consumption: list, productivity: list, nodes: list, cost_one_ton: list,
                 daily_cost_loading: list):
        self.__consumption = consumption
        self.__productivity = productivity
        self.__nodes = nodes
        self.__cost_one_ton = cost_one_ton
        self.__daily_cost_loading = daily_cost_loading

    @property
    def consumption(self) -> list:
        return self.__consumption

    @property
    def productivity(self) -> list:
        return self.__productivity

    @property
    def nodes(self) -> list:
        return self.__nodes

    @property
    def cost_one_ton(self) -> list:
        return self.__cost_one_ton

    @property
    def daily_cost_loading(self) -> list:
        return self.__daily_cost_loading

    def get_costs(self) -> list:
        all_costs = []
        for i in range(len(self.productivity)):
            row_costs = []
            for j in range(len(self.consumption)):
                row_costs.append(round(self.nodes[j][i] + self.cost_one_ton[i], 2))
            all_costs.append(row_costs)
        return all_costs

    def __str__(self):
        string = 'X(i,j) - масса песка в тоннах, перевозимая от фабрики к узлу.\n\n'
        string += 'X(i,j) ≥ 0, i = [1..%d], j = [1..%d]\n' % \
                  (len(self.productivity), len(self.consumption))

        for i, element in enumerate(self.consumption):
            equation = []
            for j in range(len(self.productivity)):
                equation.append('X(%d,%d)' % (j + 1, i + 1))
            string += '%s = %s\n' % (' + '.join(equation), element)

        for i, element in enumerate(self.productivity):
            equation = []
            for j in range(len(self.consumption)):
                equation.append('X(%d,%d)' % (i + 1, j + 1))
            string += '%s = %s\n' % (' + '.join(equation), element)

        string += 'Y(i,j) = 0 if X(i,j) = 0, i = [1..%d], j = [1..%d]\n' % \
                  (len(self.productivity), len(self.consumption))
        string += 'Y(i,j) = 1 if X(i,j) > 0, i = [1..%d], j = [1..%d]\n' % \
                  (len(self.productivity), len(self.consumption))

        objective_function = []
        for i in range(len(self.productivity)):
            for j in range(len(self.consumption)):
                objective_function.append('(%s + %s) * X(%d,%d) + %s * Y(%d,%d)' % (self.nodes[j][i],
                                                                                    self.cost_one_ton[i],
                                                                                    i + 1, j + 1,
                                                                                    self.daily_cost_loading[i],
                                                                                    i + 1, j + 1))
        string += 'F = %s\n' % (' + '.join(objective_function))
        string += 'F -> min'

        return string
