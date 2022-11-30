import sys
from KEPData import KEPData
from KEPModelLocalSolver import KEPModelLocalSolver


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

    instance = KEPData(file_path=file_path, K=3, L=3)
    print(instance)

    if method == "LS":
        model = KEPModelLocalSolver(instance=instance)
        solution = model.solve(time_limit=time_limit)
        solution.write()
    elif method == "OR":
        model = KEPModelLocalSolver(instance=instance)
        print("OR method not implemented yet")
    else:
        print("Unknown method: " + method)
        print("Available methods: LS, OR")
        exit(1)

    return 0


if __name__ == "__main__":
    main()
