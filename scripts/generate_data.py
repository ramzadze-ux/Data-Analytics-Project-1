"""Generate sample sales data: a customers dimension table and a sales fact table.

Run from the repo root:
    python3 scripts/generate_data.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
NUM_CUSTOMERS = 25
NUM_SALES = 150

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

FIRST_NAMES = {
    "Male": ["James", "John", "David", "Michael", "Daniel", "Luka", "Giorgi",
             "Thomas", "Lucas", "Noah", "Leo", "Max", "Adam"],
    "Female": ["Mary", "Linda", "Sarah", "Emma", "Olivia", "Nino", "Ana",
               "Sophie", "Mia", "Elena", "Clara", "Julia"],
}
LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Miller", "Davis", "Wilson", "Taylor",
    "Anderson", "Thomas", "Moore", "Martin", "Lee", "Walker", "Hall", "Young",
    "King", "Wright", "Lopez", "Hill", "Green", "Baker", "Adams", "Nelson",
]
LOCATIONS = [
    ("New York", "USA"), ("Chicago", "USA"), ("Austin", "USA"),
    ("London", "UK"), ("Manchester", "UK"), ("Berlin", "Germany"),
    ("Munich", "Germany"), ("Paris", "France"), ("Tbilisi", "Georgia"),
    ("Batumi", "Georgia"), ("Madrid", "Spain"), ("Toronto", "Canada"),
]
SEGMENTS = ["Consumer", "Corporate", "Small Business"]

# product_id, product_name, category, unit_price
PRODUCTS = [
    ("P001", "Wireless Mouse", "Electronics", 24.99),
    ("P002", "Mechanical Keyboard", "Electronics", 89.99),
    ("P003", "27-inch Monitor", "Electronics", 249.00),
    ("P004", "USB-C Hub", "Electronics", 39.50),
    ("P005", "Noise-Cancelling Headphones", "Electronics", 179.00),
    ("P006", "Office Chair", "Furniture", 199.00),
    ("P007", "Standing Desk", "Furniture", 429.00),
    ("P008", "Desk Lamp", "Furniture", 34.90),
    ("P009", "Bookshelf", "Furniture", 119.00),
    ("P010", "Notebook (5-pack)", "Office Supplies", 12.49),
    ("P011", "Gel Pens (12-pack)", "Office Supplies", 9.99),
    ("P012", "Printer Paper (500 sheets)", "Office Supplies", 7.80),
    ("P013", "Stapler", "Office Supplies", 14.25),
    ("P014", "Backpack", "Accessories", 59.00),
    ("P015", "Laptop Sleeve", "Accessories", 29.95),
    ("P016", "Water Bottle", "Accessories", 18.00),
]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]
CHANNELS = ["Online", "In-Store"]

START_DATE = date(2024, 1, 1)
END_DATE = date(2025, 12, 31)


def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


def make_customers():
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        gender = random.choice(["Male", "Female"])
        first = random.choice(FIRST_NAMES[gender])
        last = random.choice(LAST_NAMES)
        city, country = random.choice(LOCATIONS)
        customers.append({
            "customer_id": f"C{i:03d}",
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}{i}@example.com",
            "gender": gender,
            "age": random.randint(19, 68),
            "city": city,
            "country": country,
            "segment": random.choice(SEGMENTS),
            # Leave room so every customer can place orders after signing up
            "signup_date": random_date(START_DATE, date(2025, 6, 30)).isoformat(),
        })
    return customers


def make_sales(customers):
    # Every customer buys at least once; the rest are random repeat purchases
    buyers = customers + [random.choice(customers) for _ in range(NUM_SALES - len(customers))]
    rows = []
    for customer in buyers:
        product_id, product_name, category, unit_price = random.choice(PRODUCTS)
        quantity = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 12, 8, 5])[0]
        discount = random.choices([0.0, 0.05, 0.10, 0.20], weights=[60, 20, 15, 5])[0]
        signup = date.fromisoformat(customer["signup_date"])
        rows.append({
            "order_date": random_date(signup, END_DATE),
            "customer_id": customer["customer_id"],
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount,
            "total_amount": round(quantity * unit_price * (1 - discount), 2),
            "payment_method": random.choice(PAYMENT_METHODS),
            "channel": random.choice(CHANNELS),
        })

    rows.sort(key=lambda r: r["order_date"])
    for i, row in enumerate(rows, start=1):
        row["order_date"] = row["order_date"].isoformat()
        rows[i - 1] = {"sale_id": f"S{i:04d}", **row}
    return rows


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    random.seed(SEED)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    customers = make_customers()
    sales = make_sales(customers)
    write_csv(OUTPUT_DIR / "customers.csv", customers)
    write_csv(OUTPUT_DIR / "sales.csv", sales)
    print(f"Wrote {len(customers)} customers and {len(sales)} sales to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
