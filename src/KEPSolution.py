from pathlib import Path


class KEPSolution:
    _BASE_DIR = Path(__file__).resolve().parent.parent
    _SOLUTION_DIR = str(_BASE_DIR) + "/solution/"

    def __init__(
        self,
        instance_name: str,
        objective_value: int,
        list_of_paths: list([list([int])]),
    ):
        self.instance_name = instance_name
        self.objective_value = objective_value
        self.list_of_paths = list_of_paths
        self.name = "Solution of " + instance_name

    def __str__(self):
        return (
            self.name
            + ": objective value = "
            + str(self.objective_value)
            + ". Number of paths: "
            + str(len(self.list_of_paths))
        )

    def __repr__(self):
        return self.__str__()

    def check_fasailability(self):
        # TODO: check if the solution is feasible
        pass

    def write(self, file_path: str):
        with open(file_path, "w") as f:
            f.write(str(self.objective_value) + "\n")
            for path in self.list_of_paths:
                f.write(" ".join([str(i) for i in path]) + "\n")
