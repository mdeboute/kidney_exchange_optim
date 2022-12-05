from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from KEPData import KEPData


class KEPModelORTools:
    def _create_data_model(self):
        pass
        # TODO: implement this method with self.instance (Lin)

    # Create and register a transit callback.
    def _distance_callback(self, from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)
        return self.data_model["cost_matrix"][from_node][to_node]

    def _demand_callback(self, from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = self.manager.IndexToNode(from_index)
        return self.data_model["demands"][from_node]

    def __init__(self, instance: KEPData):
        self.instance = instance
        self.data_model = self._create_data_model()

        self.manager = pywrapcp.RoutingIndexManager(
            len(self.data_model["cost_matrix"]),
            self.data_model["num_vehicles"],
            self.data_model["starts"],
            self.data_model["ends"],
        )

        # Create Routing Model.
        self.routing = pywrapcp.RoutingModel(self.manager)

        _transit_callback_index = self.routing.RegisterTransitCallback(
            self._distance_callback
        )

        # Define cost of each arc.
        self.routing.SetArcCostEvaluatorOfAllVehicles(_transit_callback_index)

        _demand_callback_index = self.routing.RegisterUnaryTransitCallback(
            self._demand_callback
        )

        self.routing.AddDimensionWithVehicleCapacity(
            _demand_callback_index,
            0,  # null capacity slack
            self.data_model["vehicle_capacities"],  # vehicle maximum capacities
            True,  # start cumul to zero
            "Capacity",
        )

        _capacity_dimension = self.routing.GetDimensionOrDie("Capacity")

        for i in self.data_model["P"]:
            for j in self.data_model["V"]:
                if i == j:
                    continue
                index_i = self.manager.NodeToIndex(i)
                index_j = self.manager.NodeToIndex(j)
                bool_is_next_i_depot = 1
                for k in self.data_model["V"]:
                    index_k = self.manager.NodeToIndex(k)
                    bool_is_next_i_depot = bool_is_next_i_depot * (
                        self.routing.NextVar(index_i) != index_k
                    )
                bool_is_j_first = _capacity_dimension.CumulVar(index_j) == 0
                bool_same_vehicle = self.routing.VehicleVar(
                    index_i
                ) == self.routing.VehicleVar(index_j)
                bool_is_altruist_j = self.data_model["is_altruist"][j]
                bool_is_adj_i_j = self.data_model["is_adjacent"][i][j]
                bool_is_len_cycle_resp = (
                    _capacity_dimension.CumulVar(index_i) <= self.data_model["K"] - 1
                )

                self.routing.solver().Add(
                    bool_is_next_i_depot * bool_is_j_first * bool_same_vehicle
                    <= bool_is_altruist_j + (bool_is_adj_i_j * bool_is_len_cycle_resp)
                )

    def _print_solution(self, solution):
        """Prints solution on console."""

        print(f"Objective: {solution.ObjectiveValue()}")
        total_distance = 0
        total_load = 0
        for vehicle_id in range(self.data_model["num_vehicles"]):
            index = self.routing.Start(vehicle_id)
            plan_output = "Route for vehicle {}:\n".format(vehicle_id)
            route_distance = 0
            route_load = 0
            while not self.routing.IsEnd(index):
                node_index = self.manager.IndexToNode(index)
                route_load += self.data["demands"][node_index]
                plan_output += " {0} Load({1}) -> ".format(node_index, route_load)
                previous_index = index
                index = solution.Value(self.routing.NextVar(index))
                route_distance += self.routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id
                )
            plan_output += " {0} Load({1})\n".format(
                self.manager.IndexToNode(index), route_load
            )
            plan_output += "Distance of the route: {}m\n".format(route_distance)
            plan_output += "Load of the route: {}\n".format(route_load)
            print(plan_output)
            total_distance += route_distance
            total_load += route_load
        print("Total distance of all routes: {}m".format(total_distance))
        print("Total load of all routes: {}".format(total_load))

    def solve(self, time_limit: int = 600):
        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.FromSeconds(time_limit)

        # Solve the problem.
        solution = self.routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            self._print_solution(self, solution)
        else:
            print("No Solution!")
