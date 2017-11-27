class PotentialMethod:
    @staticmethod
    def perform_iteration(x: list, diffs: list) -> dict:
        results = {}

        path = PotentialMethod.get_cyclic_path(x, diffs, PotentialMethod.get_minimal(diffs))
        results['path'] = path
        corners = PotentialMethod.get_corners(path)
        results['corners'] = corners

        negative_corners = []
        for i in range(len(corners)):
            if (i + 1) % 2 == 0:
                negative_corners.append(corners[i])
        results['negative_corners'] = negative_corners

        values = []
        for corner in negative_corners:
            values.append(x[corner[0]][corner[1]])

        theta = min(values)
        results['theta'] = theta

        for i in range(len(corners)):
            if (i + 1) % 2 == 0:
                x[corners[i][0]][corners[i][1]] -= theta
            else:
                x[corners[i][0]][corners[i][1]] += theta

        return results

    @staticmethod
    def get_minimal(diffs: list) -> list:
        minimal = 0
        for row in diffs:
            values = list(filter(lambda element: element < .0, row))
            if len(values) == 0:
                continue
            value = min(values)
            if value < minimal:
                minimal = value

        for i in range(len(diffs)):
            for j in range(len(diffs[i])):
                if minimal == diffs[i][j]:
                    return [(i, j)]

    @staticmethod
    def get_cyclic_path(x: list, diffs: list, path: list) -> list or None:
        i, j = path[-1]

        if j + 1 < len(x[i]) and PotentialMethod.is_available(path, i, j + 1):
            result = PotentialMethod.get_cyclic_path_with_indexes(x, diffs, path, i, j + 1)
            if result is not None:
                return result

        if i + 1 < len(x) and PotentialMethod.is_available(path, i + 1, j):
            result = PotentialMethod.get_cyclic_path_with_indexes(x, diffs, path, i + 1, j)
            if result is not None:
                return result

        if j - 1 >= 0 and PotentialMethod.is_available(path, i, j - 1):
            result = PotentialMethod.get_cyclic_path_with_indexes(x, diffs, path, i, j - 1)
            if result is not None:
                return result

        if i - 1 >= 0 and PotentialMethod.is_available(path, i - 1, j):
            result = PotentialMethod.get_cyclic_path_with_indexes(x, diffs, path, i - 1, j)
            if result is not None:
                return result

    @staticmethod
    def get_cyclic_path_with_indexes(x: list, diffs: list, path: list, i: int, j: int) -> list or None:
        if len(path) > 1:
            if i == path[0][0] and j == path[0][1] and len(path) < 4:
                return
            if PotentialMethod.is_turn(path, (i, j)) and (diffs[path[-1][0]][path[-1][1]] != .0 or
                                                          x[path[-1][0]][path[-1][1]] == .0):
                return
        local_path = path[:]
        local_path.append((i, j))
        if i == path[0][0] and j == path[0][1]:
            return local_path
        else:
            return PotentialMethod.get_cyclic_path(x, diffs, local_path)

    @staticmethod
    def is_available(path: list, i: int, j: int) -> bool:
        if path.count((i, j)) > 0 and not (path[0][0] == i and path[0][1] == j):
            index = path.index((i, j))
            return path[index - 1][0] != path[-2][0] and path[index - 1][1] != path[-2][1]
        return True

    @staticmethod
    def is_turn(path: list, possible: tuple) -> bool:
        return (path[-2][0] == path[-1][0] and path[-1][1] == possible[1]) or \
               (path[-2][1] == path[-1][1] and path[-1][0] == possible[0])

    @staticmethod
    def get_corners(path: list) -> list or None:
        if path is not None:
            corners = [path[0]]
            for i in range(len(path) - 2):
                if PotentialMethod.is_turn(path[i:i + 2], path[i + 2]):
                    corners.append(path[i + 1])
            return corners
