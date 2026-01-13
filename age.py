import datetime


def main():
    name = input("Enter your name: ").strip()
    birth_year_str = input("Enter your birth year (e.g., 1990): ").strip()
    try:
        birth_year = int(birth_year_str)
    except ValueError:
        print("Invalid birth year. Please enter a valid number.")
        return

    current_year = datetime.date.today().year
    age = current_year - birth_year

    if age < 0:
        print(f"Hello, {name}! That birth year ({birth_year}) is in the future.")
    else:
        print(f"Hello, {name}! You are {age} years old.")


if __name__ == "__main__":
    main()
