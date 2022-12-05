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
                for line in data[2 : 2 + nb_vertices]:
                    if "Alturist" in line:
                        list_of_altruists.append(int(line.split(" ")[-1]))
                # from line 12 skip all the lines that begins with #
                data = [line for line in data[2:] if not line.startswith("#")]
                # now the data looks like this: "1,5,1.0" where 1 is the source vertex, 5 is the destination vertex and 1.0 is the weight
                # save all this information in an adjacency matrix
                adjacency_matrix = np.full((nb_vertices + 1, nb_vertices + 1), 0)
                # and in a list of edges
                list_of_edges = []
                cpt = 0
                for line in data:
                    source, destination, weight = line.split(",")
                    adjacency_matrix[int(source)][int(destination)] = int(float(weight))
                    if float(weight) > 0:
                        list_of_edges.append(
                            Edge(int(source), int(destination), int(float(weight)), cpt)
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
        except Exception as e:
            print("Error: " + str(e) + ".")
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
        if L < K:
            print("Error: L must be greater than or equal to K. With K > 2.")
            exit(1)
        self.K = K
        self.L = L
        if "\\" in file_path:
            self.name = file_path.split("\\")[-1].split(".")[0]
        else:
            self.name = file_path.split("/")[-1].split(".")[0]

    def __str__(self):
        return (
            "Instance n°"
            + self.name
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
