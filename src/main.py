import sys
from KEPModel import KEPModel


def main():
    argv = sys.argv[1:]

    if len(argv) != 1:
        print("Usage: python3 main.py <instance_file>")
        exit(1)

    file_path = argv[0]

    instance = KEPModel(file_path=file_path)

    return 0


if __name__ == "__main__":
    main()
