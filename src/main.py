import sys
from KEPData import KEPData
from KEPModelLocalSolver import KEPModelLocalSolver
from KEPModelORTools import KEPModelORTools


def print_usage():
    print("Usage: python3 main.py <instance_file> <method> (<time_limit>)")
    print("Where <method> is one of: LS or OR")
    print("<time_limit> is optional, its default value is set to 600 seconds")
    exit(1)


def main():
    argv = sys.argv[1:]
    if len(argv) < 2 or len(argv) > 3:
        print_usage()

    file_path = argv[0]
    method = argv[1]
    time_limit = 600
    if len(argv) == 3:
        time_limit = int(argv[2])

    if method == "LS":
        instance = KEPData(file_path=file_path, K=3, L=5)
        print(instance)
        model = KEPModelLocalSolver(instance=instance)
        model.solve(time_limit=time_limit)
        #solution = model.solve(time_limit=time_limit)
        #solution.write()
    elif method == "OR":
        instance = KEPData(file_path=file_path, K=3, L=5)
        print(instance)
        model = KEPModelORTools(instance=instance)
        solution = model.solve(time_limit=time_limit)
        if solution.check_feasibility():
            solution.write()
        else:
            print("Solution is not feasible!")
            exit(1)
    else:
        print("Unknown method: " + method)
        print("Available methods: LS, OR")
        exit(1)

    return 0


if __name__ == "__main__":
    main()
