import sys
from KEPData import KEPData


def print_usage():
    print("Usage: python3 main.py <instance_file>")
    exit(0)


def main():
    argv = sys.argv[1:]

    if len(argv) != 1:
        print_usage()

    if "-h" in argv or "--help" in argv:
        print_usage()

    file_path = argv[0]
    instance = KEPData(file_path=file_path)
    print(instance)

    return 0


if __name__ == "__main__":
    main()
