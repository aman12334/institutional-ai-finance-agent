import sys
from run_report import run


def main():
    args = sys.argv[1:]

    if len(args) % 2 != 0:
        print("Usage: python cli.py <TICKER> <LABEL> [<TICKER> <LABEL> ...]")
        sys.exit(1)

    companies = [(args[i], args[i+1]) for i in range(0, len(args), 2)]

    run(companies)


if __name__ == "__main__":
    main()
