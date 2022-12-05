from pathlib import Path
from KEPData import KEPData


class KEPSolution:
    _BASE_DIR = Path(__file__).resolve().parent.parent
    _SOLUTION_DIR = _BASE_DIR / "solutions"
    _SOLUTION_DIR.mkdir(parents=True, exist_ok=True)

    def __init__(
        self,
        instance: KEPData,
        objective_value: int,
        list_of_paths: list([list([int])]),
    ):
        self.instance = instance
        self.objective_value = objective_value
        self.list_of_paths = list_of_paths

    def __str__(self):
        return (
            "Solution n°"
            + self.instance.name
            + ": objective value = "
            + str(self.objective_value)
            + ". Number of paths: "
            + str(len(self.list_of_paths))
        )

    def __repr__(self):
        return self.__str__()

    def _is_cycle(self, path: list([int])) -> bool:
        return path[0] == path[-1]

    def check_feasibility(self):
        # check if the solution is feasible
        # the maximum length of a path is L
        # the maximum length of a cycle is K

        # check if the length of each path is less or equal to L
        for path in self.list_of_paths:
            if not self._is_cycle(path) and len(path) > self.instance.L:
                print(
                    (
                        "Error: path "
                        + str(path)
                        + " is too long. L = "
                        + str(self.instance.L)
                    )
                )
                return False

        # check if the length of each cycle is less or equal to K
        for path in self.list_of_paths:
            if self._is_cycle(path) and len(path) - 1 > self.instance.K:
                print(
                    (
                        "Error: cycle "
                        + str(path)
                        + " is too long. K = "
                        + str(self.instance.K)
                    )
                )
                return False

        # check that each node of a path are adjacent
        for path in self.list_of_paths:
            for i in range(len(path) - 1):
                if path[i + 1] not in self.instance.get_adjacency_list()[path[i]]:
                    print(
                        "Error: nodes "
                        + str(path[i])
                        + " and "
                        + str(path[i + 1])
                        + " are not adjacent."
                    )
                    return False

        return True

    def write(self):
        file_path = KEPSolution._SOLUTION_DIR / (
            "result_" + self.instance.name + ".txt"
        )
        try:
            with open(file_path, "w") as f:
                f.write(str(self.objective_value) + "\n")
                for path in self.list_of_paths:
                    f.write(" ".join([str(i) for i in path]) + "\n")
        except Exception as e:
            print("Error: " + str(e))
            exit(1)
        print("Solution written to " + str(file_path))
