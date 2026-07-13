import os
from database import create_tables


def main():
    create_tables()

    if os.path.exists("database/expense.db"):
        print("Database created successfully!")
        print("Tables are ready.")
    else:
        print("Database creation failed.")


if __name__ == "__main__":
    main()
