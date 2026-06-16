from .calculator import add, divide


def main() -> None:
    print("GitHub Enterprise Learning Lab")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 / 2 = {divide(10, 2)}")


if __name__ == "__main__":
    main()

