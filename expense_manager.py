import json
import os
import uuid
from datetime import datetime


DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "expenses.json"
)


def load_expenses():
    """Load expenses from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Expense data must be a list.")

        for expense in data:
            if "id" not in expense:
                expense["id"] = str(uuid.uuid4())

        return data

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise RuntimeError(f"Could not load expenses: {error}")


def save_expenses(expenses):
    """Save expenses permanently to the JSON file."""
    temp_file = DATA_FILE + ".tmp"

    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)

        os.replace(temp_file, DATA_FILE)

    except OSError as error:
        if os.path.exists(temp_file):
            os.remove(temp_file)

        raise RuntimeError(f"Could not save expenses: {error}")


def add_expense(
    expenses,
    title,
    category,
    amount,
    expense_date,
    description
):
    """Add a new expense."""
    new_expense = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "category": category.strip(),
        "amount": round(float(amount), 2),
        "date": expense_date.strip(),
        "description": description.strip()
    }

    expenses.append(new_expense)
    save_expenses(expenses)

    return expenses


def update_expense(
    expenses,
    record_id,
    title,
    category,
    amount,
    expense_date,
    description
):
    """Update an existing expense."""
    for expense in expenses:
        if expense["id"] == record_id:
            expense["title"] = title.strip()
            expense["category"] = category.strip()
            expense["amount"] = round(float(amount), 2)
            expense["date"] = expense_date.strip()
            expense["description"] = description.strip()

            save_expenses(expenses)
            return expenses

    raise ValueError("Expense record was not found.")


def delete_expense(expenses, record_id):
    """Delete an expense."""
    updated_expenses = [
        expense for expense in expenses
        if expense["id"] != record_id
    ]

    if len(updated_expenses) == len(expenses):
        raise ValueError("Expense record was not found.")

    save_expenses(updated_expenses)

    return updated_expenses


def validate_date(date_text):
    """Validate date in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            "Invalid date. Please use YYYY-MM-DD format."
        )