import sys
from KEPData import KEPData


def main():
    argv = sys.argv[1:]

    if len(argv) != 1:
        print("Usage: python3 main.py <instance_file>")
        exit(1)

    file_path = argv[0]

    instance = KEPData(file_path=file_path)
    print(instance)

    return 0


if __name__ == "__main__":
    main()
