import itertools


class Edge:
    def __init__(self, start: int, end: int, weight):
        self.start: int = start
        self.end: int = end
        self.weight = weight

    def __str__(self):
        return f"{self.start + 1}-{self.end + 1}; Вес-{self.weight}"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.weight == other.weight


class Result:
    def __init__(self, sum_of_weight: int, edges: list[Edge]):
        self.sum_of_weight: int = sum_of_weight
        self.edges: list[Edge] = edges
        self.edges_str = self.stringify_result()

    def stringify_result(self) -> str:
        str_v: list[str] = list()

        for i in self.edges:
            str_v.append(f"{i.start + 1}-{i.end + 1}")

        return " ".join(str_v)


class Graph:
    def __init__(self, matrix: list[list[int]], start: int, end: int):
        self.edges: list[Edge] = self.create_edges(matrix)
        self.start: int = start
        self.end: int = end
        self.resultEdges: list[Edge] = list()
        self.selectedEdges: list[Edge] = list()
        self.usedEdges: list[bool] = list()
        self.end_edge: Edge = None

    @staticmethod
    def create_edges(matrix: list[list[int]]) -> list[Edge]:
        vertexes: list[Edge] = list()

        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix[i])):
                if matrix[i][j] != 0:
                    v = Edge(start=i, end=j, weight=matrix[i][j])
                    vertexes.append(v)

        return vertexes

    def sum_of_weights(self) -> int:
        wights_sum = 0

        for v in self.selectedEdges:
            wights_sum = wights_sum + v.weight

        return wights_sum

    def find_shortest_path(self) -> Result:
        totalSum: int = 2000000000

        for counter in itertools.product([0, 1], repeat=len(self.edges)):
            for i in range(len(counter)):
                if counter[i] == 1:
                    self.selectedEdges.append(self.edges[i])
                    self.usedEdges.append(False)

            start_edge = self.get_start_edge()

            if start_edge is None:
                self.selectedEdges.clear()
                self.usedEdges.clear()
                continue

            current_sum = 0

            self.path_is_exists(start_edge)

            if self.end_edge is not None:
                current_sum = self.sum_of_weights()

                if current_sum < totalSum:
                    totalSum = current_sum
                    self.resultEdges.clear()
                    self.resultEdges = self.selectedEdges.copy()

            self.selectedEdges.clear()
            self.usedEdges.clear()
            self.end_edge = None

        return Result(totalSum, self.resultEdges)

    def path_is_exists(self, prev_edge: Edge):
        if prev_edge.start == self.end or prev_edge.end == self.end:
            self.end_edge = prev_edge
            return

        for i in range(len(self.selectedEdges)):
            if self.usedEdges[i]:
                continue

            if prev_edge.start == self.selectedEdges[i].start or prev_edge.start == self.selectedEdges[i].end:
                self.usedEdges[i] = True
                self.path_is_exists(self.selectedEdges[i])
            elif prev_edge.end == self.selectedEdges[i].start or prev_edge.end == self.selectedEdges[i].end:
                self.usedEdges[i] = True
                self.path_is_exists(self.selectedEdges[i])

    def get_start_edge(self) -> Edge | None:
        for i in range(len(self.selectedEdges)):
            if self.selectedEdges[i].start == self.start or self.selectedEdges[i].end == self.start:
                self.usedEdges[i] = True
                return self.selectedEdges[i]


def get_next_vertex(vertexes: list[Edge], next_vertex: int) -> Edge | None:
    for v in vertexes:
        if v.start == next_vertex or v.end == next_vertex:
            return v
