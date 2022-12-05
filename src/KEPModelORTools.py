from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from KEPData import KEPData


class KEPModelORTools:
    def _create_data_model(self):
        pass
        # TODO: implement this method with self.instance (Lin)

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
