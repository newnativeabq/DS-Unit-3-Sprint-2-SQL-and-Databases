import sqlite3


# Helper Functions
def execute_fetchall_sqlite_query(connection, query):
    cursor = connection.cursor()
    return cursor.execute(query).fetchall()

# Part 1B: Queries
connection = sqlite3.connect('northwind_small(1).sqlite3')

# Get table names for reference
query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
print(query, execute_fetchall_sqlite_query(connection, query))

## What are the ten most expensive items (per unit price) in the database and their suppliers?
query = """
SELECT ProductName, UnitPrice
FROM Product
ORDER BY UnitPrice DESC
LIMIT 10
"""
print(query, execute_fetchall_sqlite_query(connection, query))

## What is the average age of an employee at the time of their hiring? (Hint: a lot of arithmetic works with dates.)
query = """
SELECT HireDate-BirthDate
FROM Employee
"""
print(query, execute_fetchall_sqlite_query(connection, query))

## (Stretch) How does the average age of employee at hire vary by city?
query = """
SELECT AVG(HireDate-BirthDate) as Age_At_Hire, City
FROM Employee
GROUP BY City
"""
print(query, execute_fetchall_sqlite_query(connection, query))

## What are the ten most expensive items (per unit price) in the database and their suppliers?
query = """
SELECT Product.ProductName, Product.UnitPrice, Supplier.CompanyName
FROM Product INNER JOIN Supplier
ON Product.SupplierId = Supplier.Id
ORDER BY Product.UnitPrice DESC
LIMIT 10
"""
print(query, execute_fetchall_sqlite_query(connection, query))

## What is the largest category (by number of unique products in it)?
query = """
SELECT COUNT(Product.CategoryID) as NumProd, Category.CategoryName
FROM Product JOIN Category
ON Product.CategoryId = Category.Id
GROUP BY CategoryID
ORDER BY  NumProd DESC
LIMIT 1
"""
print(query, execute_fetchall_sqlite_query(connection, query))

connection.close()