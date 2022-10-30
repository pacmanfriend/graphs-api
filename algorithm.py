import itertools


# Ребро графа
class Vertex:
    def __init__(self, start: int, end: int, weight):
        self.start: int = start
        self.end: int = end
        self.weight = weight

    def __str__(self):
        return f"{self.start}-{self.end}; Вес-{self.weight}"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.weight == other.weight


class Result:
    def __init__(self, sum_of_weight: int, vertexes: list[Vertex]):
        self.sum_of_weight: int = sum_of_weight
        self.vertexes: list[Vertex] = vertexes

    def stringify_result(self) -> str:
        str_v: list[str] = list()

        for i in self.vertexes:
            str_v.append(i.__str__())

        return " ".join(str_v)


def create_vertexes(matrix: list[list[int]]) -> list[Vertex]:
    vertexes: list[Vertex] = list()

    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix[i])):
            if matrix[i][j] != 0:
                v = Vertex(start=i, end=j, weight=matrix[i][j])
                vertexes.append(v)

    return vertexes


def path_is_exists(vertexes: list[Vertex], vertex: Vertex, end: int) -> bool:
    if len(vertexes) == 0:
        if vertex.start == end or vertex.end == end:
            return True
        else:
            return False
    else:
        next_vertex = get_next_vertex(vertexes, vertex)

        if next_vertex is None:
            return False
        else:
            vertexes.remove(vertex)
            path_is_exists(vertexes, next_vertex, end)


def get_next_vertex(vertexes: list[Vertex], vertex: Vertex) -> Vertex | None:
    for v in vertexes:
        if vertex.start == v.end or vertex.end == v.start:
            return v


def get_start_vertex(vertexes: list[Vertex], start: int) -> Vertex | None:
    for vertex in vertexes:
        if vertex.start == start or vertex.end == start:
            return vertex


def sum_weights(vertexes: list[Vertex]) -> int:
    sum_of_weights = 0

    for v in vertexes:
        sum_of_weights += v.weight

    return sum_of_weights


def finding_shortest_path(matrix: list[list[int]], start: int, end: int) -> Result:
    vertexes: list[Vertex] = create_vertexes(matrix)

    totalSum: int = 10000000
    result_vertexes: list[Vertex] = list()

    for counter in itertools.product([0, 1], repeat=len(vertexes)):
        selectedVertexes: list[Vertex] = list()

        for i in range(len(counter)):
            if counter[i] == 1:
                selectedVertexes.append(vertexes[i])

        start_vertex = get_start_vertex(selectedVertexes, start)

        if start_vertex is None:
            continue

        selectedVertexes.remove(start_vertex)

        if path_is_exists(selectedVertexes, start_vertex, end):
            current_sum = sum_weights(selectedVertexes)

            if current_sum < totalSum:
                totalSum = current_sum
                result_vertexes = selectedVertexes.copy()

        selectedVertexes.clear()

    return Result(sum_of_weight=totalSum, vertexes=result_vertexes)
