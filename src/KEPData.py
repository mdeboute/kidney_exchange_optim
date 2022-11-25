import numpy as np


class KEPData:
    def __parse__(file_path: str):
        try:
            with open(file_path, "r") as file:
                data = file.read()
                # skip the 9 first lines
                data = data.splitlines()[9:]
                # split the line 10 by ":" and save the second part as the number of vertices
                nb_vertices = int(data[0].split(":")[1])
                # split the line 11 by ":" and save the second part as the number of edges
                nb_edges = int(data[1].split(":")[1])
                # from line 11 skip all the lines that begins with #
                data = [line for line in data[2:] if not line.startswith("#")]
                # now the data looks like this: "1,5,1.0" where 1 is the source vertex, 5 is the destination vertex and 1.0 is the weight
                # save all this information in an adjacency matrix
                adjacency_matrix = np.full((nb_vertices + 1, nb_vertices + 1), -1)
                for line in data:
                    source, destination, weight = line.split(",")
                    adjacency_matrix[int(source)][int(destination)] = float(weight)
            file.close()
            return nb_vertices, nb_edges, adjacency_matrix
        except FileNotFoundError:
            print("Error: File not found.")
            exit(1)

    def __init__(self, file_path: str, K: int, L: int):
        KEPData.__parse__(file_path)
        self.nb_vertices, self.nb_edges, self.adjacency_matrix = KEPData.__parse__(
            file_path
        )
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
        )

    def __repr__(self):
        return self.__str__()

    def get_number_of_altruists(self):
        # count the number of 0 in the adjacency matrix divided by the number of vertices
        return int(
            np.ceil(np.count_nonzero(self.adjacency_matrix == 0) / self.nb_vertices)
        )

    def print_adjacency_matrix(self):
        print(self.adjacency_matrix)
