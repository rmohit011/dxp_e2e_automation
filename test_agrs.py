import sys


def main():
    # Check if there are enough command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py [arg1] [arg2] ...")
        return

    # Access and print the runtime arguments
    print("Runtime arguments:")
    for i, arg in enumerate(sys.argv[1:], start=1):
        print(f"Argument {i}: {arg}")


if __name__ == "__main__":
    main()
