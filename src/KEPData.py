import numpy as np


class Edge:
    def __init__(self, node_1, node_2, weight, edge_id):
        self.node_1 = node_1
        self.node_2 = node_2
        self.weight = weight
        self.edge_id = edge_id

    def __str__(self):
        return f"({self.node_1}, {self.node_2}, {self.weight})"

    def __repr__(self):
        return str(self)


class KEPData:
    def _parse(file_path: str):
        try:
            with open(file_path, "r") as file:
                data = file.read()
                # skip the 9 first lines
                data = data.splitlines()[9:]
                # split the line 10 by ":" and save the second part as the number of vertices
                nb_vertices = int(data[0].split(":")[1])
                # split the line 11 by ":" and save the second part as the number of edges
                nb_edges = int(data[1].split(":")[1])
                # from line 12 to line 12 + nb_vertices - 1, count the number of line with "Alturist" and put it in a list
                list_of_altruists = []
                for line in data[3 : nb_vertices + 2]:
                    if "Alturist" in line:
                        list_of_altruists.append(int(line.split(" ")[-1]))
                # from line 11 skip all the lines that begins with #
                data = [line for line in data[2:] if not line.startswith("#")]
                # now the data looks like this: "1,5,1.0" where 1 is the source vertex, 5 is the destination vertex and 1.0 is the weight
                # save all this information in an adjacency matrix
                adjacency_matrix = np.full((nb_vertices + 1, nb_vertices + 1), -1)
                # and in a list of edges
                list_of_edges = []
                cpt = 0
                for line in data:
                    source, destination, weight = line.split(",")
                    adjacency_matrix[int(source)][int(destination)] = float(weight)
                    list_of_edges.append(
                        Edge(int(source), int(destination), float(weight), cpt)
                    )
                    cpt += 1
            file.close()
            return (
                nb_vertices,
                nb_edges,
                list_of_altruists,
                adjacency_matrix,
                list_of_edges,
            )
        except FileNotFoundError:
            print("Error: File not found.")
            exit(1)

    def __init__(self, file_path: str, K: int, L: int):
        KEPData._parse(file_path)
        (
            self.nb_vertices,
            self.nb_edges,
            self.list_of_altruists,
            self.adjacency_matrix,
            self.list_of_edges,
        ) = KEPData._parse(file_path)
        # L must be greater than K
        if L <= K:
            print("Error: L must be greater than K. With K > 2.")
            exit(1)
        self.K = K
        self.L = L
        self.name = "Instance n°" + file_path.split("/")[-1].split(".")[0]

    def __str__(self):
        return (
            self.name
            + ": graph with "
            + str(self.nb_vertices)
            + " vertices and "
            + str(self.nb_edges)
            + " edges."
            + " K = "
            + str(self.K)
            + " and L = "
            + str(self.L)
            + ". Number of alturists: "
            + str(len(self.list_of_altruists))
        )

    def __repr__(self):
        return self.__str__()

    def get_adjacency_list(self):
        adj = [[] for _ in range(self.nb_vertices + 1)]
        for edge in self.list_of_edges:
            adj[edge.node_1].append(edge.node_2)
        return adj

    def get_all_possible_cycles(self):
        # get all possible cycles of the graph that does not contain any alturist
        # and that has a maximal length equal to K
        adj = self.get_adjacency_list()
        cycles = []
        for i in range(1, self.nb_vertices + 1):
            for j in adj[i]:
                if i != j:
                    cycles.append([i, j])
        for i in range(2, self.K):
            new_cycles = []
            for cycle in cycles:
                for j in adj[cycle[-1]]:
                    if j not in cycle:
                        new_cycles.append(cycle + [j])
            cycles = new_cycles
        # remove all the cycles that contains an alturist
        for cycle in cycles:
            if any([node in self.list_of_altruists for node in cycle]):
                cycles.remove(cycle)
        return cycles

        # TODO: to verify lmao
