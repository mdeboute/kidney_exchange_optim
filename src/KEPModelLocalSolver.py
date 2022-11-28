from localsolver import LocalSolver as ls
from KEPData import KEPData


class KEPModelLocalSolver:
    def __init__(self, instance: KEPData):

        # set list size to upper bound + 1 that is unsatisfied couples
        self.nb_lists = int((instance.nb_vertices / 2) + 1)

        self.model = ls.model

        # Sequence of customers visited by each truck.
        self.couples_sequences = [
            self.model.list(instance.nb_vertices) for k in range(self.nb_lists)
        ]

        # All sequences needs to be disjoints, including unsatisfied couples
        self.model.constraint(self.model.partition(self.couples_sequences))

        # Create distance as an array to be able to access it with an "at" operator
        self.weights_array = self.model.array()
        for n in range(instance.nb_vertices):
            self.weights_array.add_operand(self.model.array(instance.list_of_edges[n]))

        # TODO: re implement with the data struct

        self.model.maximize()

        self.model.close()

    def solve(
        self,
        verbose: bool = True,
        time_limit: int = 600,
    ):

        ls.param.time_limit = time_limit

        ls.solve()

        for k in range(self.nb_lists):
            _sequence_to_text = ""
            if len(self.couples_sequences[k].value) == 1:
                continue
            for c in self.couples_sequences[k].value:
                if c >= self.nb_vertices_first:
                    c = "*"
                _sequence_to_text += str(c) + " "
            print(_sequence_to_text)
