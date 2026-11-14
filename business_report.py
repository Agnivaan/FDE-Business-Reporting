import sqlite3
import csv

DB_PATH = r"C:\Users\Administrator\Downloads\FDE\Day10\business.db"

print("================================")
print("   BUSINESS DATABASE REPORT")
print("================================")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Total Customers
cursor.execute("SELECT COUNT(*) FROM customers")
total_customers = cursor.fetchone()[0]

# Total Orders
cursor.execute("SELECT COUNT(*) FROM orders")
total_orders = cursor.fetchone()[0]

# Total Revenue
cursor.execute("SELECT SUM(amount) FROM orders")
total_revenue = cursor.fetchone()[0] or 0

# Average Order Value
cursor.execute("SELECT AVG(amount) FROM orders")
average_order = cursor.fetchone()[0] or 0

print("Total Customers:", total_customers)
print("Total Orders:", total_orders)
print("Total Revenue:", total_revenue)
print("Average Order Value:", round(average_order, 2))

# Customer-wise Revenue Analysis

print("\nCUSTOMER-WISE REVENUE")
print("-------------------------")

query = """
SELECT
    customers.name,
    SUM(orders.amount)
FROM customers
INNER JOIN orders
ON customers.id = orders.customer_id
GROUP BY customers.id, customers.name
ORDER BY SUM(orders.amount) DESC
"""

cursor.execute(query)

customer_data = cursor.fetchall()

for customer in customer_data:
    print("Customer:", customer[0])
    print("Revenue: Rs.", customer[1])
    print("-------------------------")

print("\nHIGH VALUE CUSTOMERS")
print("-------------------------")

query = """
SELECT customers.name, SUM(orders.amount)
FROM customers
INNER JOIN orders
ON customers.id = orders.customer_id
GROUP BY customers.id, customers.name
HAVING SUM(orders.amount) > ?
"""

cursor.execute(query, (100000,))

for customer in cursor.fetchall():
    print(customer[0], ":", customer[1])

# Export Customer Revenue to CSV

with open("customer_revenue.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow(["Customer Name", "Total Revenue"])

    writer.writerows(customer_data)

print("\nCSV REPORT CREATED SUCCESSFULLY!")

# Minimum and Maximum Order Analysis

print("\nORDER VALUE ANALYSIS")
print("-------------------------")

query = """
SELECT
    MIN(amount),
    MAX(amount),
    COUNT(amount)
FROM orders
"""

cursor.execute(query)

result = cursor.fetchone()

print("Minimum Order:", result[0])
print("Maximum Order:", result[1])
print("Number of Orders:", result[2])

# High Value Order Report

print("\nHIGH VALUE ORDER REPORT")
print("-------------------------")

query = """
SELECT
    customers.name,
    orders.product,
    orders.amount
FROM customers
INNER JOIN orders
ON customers.id = orders.customer_id
WHERE orders.amount >= ?
ORDER BY orders.amount DESC
"""

cursor.execute(query, (150000,))

high_value_orders = cursor.fetchall()

for order in high_value_orders:
    print("Customer:", order[0])
    print("Product:", order[1])
    print("Amount: Rs.", order[2])
    print("-------------------------")

connection.close()