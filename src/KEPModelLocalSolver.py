import localsolver
from KEPData import KEPData
#from KEPSolution import KEPSolution

class KEPModelLocalSolver:
    def __init__(self, instance: KEPData):
        self.instance = instance
        # set list size to upper bound + 1 that is unsatisfied couples
        self.nb_lists = int((self.instance.nb_vertices / 2) + 1)
        print("nbr de list=" + str(self.nb_lists))
        #create virtual vertices
        self.nb_vertices_first = self.instance.nb_vertices
        self.nb_vertices = int(self.nb_vertices_first*1.5)
        print("n origin=" + str(self.nb_vertices_first) + "\t n=" + str(self.nb_vertices))

        self.adjacency_matrix = [[0 for i in range(self.nb_vertices)] for j in range(self.nb_vertices)]
        self.weights_matrix = [[0 for i in range(self.nb_vertices)] for j in range(self.nb_vertices)]

        for i in range(len(self.instance.adjacency_matrix)):
            for j in range(len(self.instance.adjacency_matrix[i])):
                self.adjacency_matrix[i-1][j-1] = int(instance.adjacency_matrix[i][j]!=0)
                self.weights_matrix[i-1][j-1] = instance.adjacency_matrix[i][j]

        for i in range(self.nb_vertices_first, self.nb_vertices):
            self.adjacency_matrix[i][i] = 1

        self.list_of_altruists = [0 for i in range(self.nb_vertices)]
        for i in instance.list_of_altruists :
            self.list_of_altruists[i-1] = 1
        print("list of altruits :")
        print(self.list_of_altruists)

        for l in self.adjacency_matrix:
            line = ""
            for i in l:
                line += str(i) + " "
            print(line)
        print(" /// ")
        for l in self.weights_matrix:
            line = ""
            for i in l:
                line += str(i) + " "
            print(line)

    def solve(
        self,
        verbose: bool = True,
        time_limit: int = 600,
    ):
#->KEPSolution

        with localsolver.LocalSolver() as ls:

            self.model = ls.model

            # Sequence of customers visited by each truck.
            self.couples_sequences = [ self.model.list(self.nb_vertices) for k in range(self.nb_lists)]

            # All sequences needs to be disjoints, including unsatisfied couples
            self.model.constraint(self.model.partition(self.couples_sequences))

            # Create data as arrays to be able to access it with an "at" operator
            _weights_array = self.model.array()
            for n in range(self.nb_vertices):
                _weights_array.add_operand(self.model.array(self.weights_matrix[n]))
            _altruist_array = self.model.array(self.list_of_altruists)
            _donnors_array = self.model.array(range(self.nb_vertices))
            _adjacency_matrix_array = self.model.array()
            for n in range(self.nb_vertices):
                _adjacency_matrix_array.add_operand(self.model.array(self.adjacency_matrix[n]))

            _sequences_weights = [0] * self.nb_lists
            _sequences_weights[self.nb_lists-1] = 0

            for k in range(self.nb_lists-1):
                sequence = self.couples_sequences[k]
                c = self.model.count(sequence)
                is_altruist_sequence = self.model.at(_altruist_array,sequence[0])

                #size limit
                limit = self.instance.K + (self.instance.L-self.instance.K)*is_altruist_sequence
                self.model.constraint(c <= limit)

                #edges existance
                couples_selector = self.model.lambda_function(lambda i: self.model.at(_adjacency_matrix_array,sequence[i],sequence[i+1]))
                self.model.constraint(self.model.sum(self.model.range(0, c-1), couples_selector) >= c-1)

                #return edge existance
                final_is_existing = self.model.at(_adjacency_matrix_array,sequence[c-1],sequence[0])
                self.model.constraint((final_is_existing + is_altruist_sequence) == 1)
                #self.model.constraint((final_is_existing) == 1)

                #objective calculations
                weight_selector = self.model.lambda_function(lambda i: self.model.at(_weights_array, sequence[i], sequence[i + 1]))
                _sequences_weights[k] = self.model.sum(self.model.range(0, c-1), weight_selector) + (1-is_altruist_sequence)*self.model.at(_weights_array, sequence[c-1], sequence[0])
                #_sequences_weights[k] = self.model.sum(self.model.range(0, c-1), weight_selector) + self.model.at(_weights_array, sequence[c-1], sequence[0])

            # Total distance traveled
            total_weight = self.model.sum(_sequences_weights)
            self.model.maximize(total_weight)

            self.model.close()

            ls.param.time_limit = time_limit
            ls.solve()

            print("nb lists" + str(self.nb_lists))
            for k in range(self.nb_lists):
                _sequence_to_text = ""
                #if len(self.couples_sequences[k].value) == 1:
                #    continue
                for c in self.couples_sequences[k].value:
                    if c >= self.nb_vertices_first:
                        c = "*"
                    _sequence_to_text += str(c) + " "
                print(_sequence_to_text)
        #return KEPSolution()#!!!
