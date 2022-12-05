from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from KEPData import KEPData


class KEPModelORTools:
    def _create_data_model(self):
        """Stores the data for the problem."""
        max_weight = max([max(self.instance.adjacency_matrix[i]) for i in range(nb_Vertices)])
        U = 10 * max_weight * self.instance.nb_edges   # distance between non adjacent vertices
        data_model= {}
        data_model['N'] = self.instance.list_of_altruists()
        data_model['V'] = [i for i in range(1, self.instance.nb_vertices+1)]
        data_model['P'] = [i for i in data_model['V']) if i not in data_model['N']]
        data_model['L'] = self.instance.L
        data_model['K'] = self.instance.K
        data_model['U'] = U
        data_model['cost_matrix'] = [] 
        for i in range(self.instance.nb_vertices+1):
            cost_line_i = []
            for j in range(self.instance.nb_vertices+1):
                if i==j:
                    cost_line_i.append(0)
                elif i==0 or j==0:
                    cost_line_i.append(max_weight)
                elif self.instance.adjacency_matrix[i-1][j-1]==0:
                    cost_line_i.append(U)
                else:
                    cost_line_i.append(max_weight - self.instance.adjacency_matrix[i-1][j-1])
            data_model['cost_matrix'].append(cost_line_i)

        data_model['num_vehicles'] = len(data_model['V'])
        data_model['demands'] = [0] + [1 for i in range(len(data_model['V']))]
        data_model['vehicle_capacities'] = [data_model['L'] for i in range(data_model['num_vehicles'])]
        data_model['depot'] = 0

        return data_model

    def __init__(self, instance: KEPData):
        self.instance = instance
        self.data_model = self._create_data_model()

        manager = pywrapcp.RoutingIndexManager(
            len(self.data_model["cost_matrix"]),
            self.data_model["num_vehicles"],
            self.data_model["starts"],
            self.data_model["ends"],
        )

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)
        # TODO: implement this method with self.instance (Martin)
