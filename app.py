from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)


# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="online_bookstore",
        user="postgres",
        password="Ant@ra01",
        port="5432"
    )


# Home
@app.route("/")
def home():
    return "Online Bookstore API is running!"


# Books
@app.route("/api/books")
def get_books():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Books ORDER BY Book_ID")
    rows = cur.fetchall()

    columns = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    return jsonify([
        dict(zip(columns, row))
        for row in rows
    ])


# Customers
@app.route("/api/customers")
def get_customers():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Customers ORDER BY Customer_ID")
    rows = cur.fetchall()

    columns = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    return jsonify([
        dict(zip(columns, row))
        for row in rows
    ])


# Orders
@app.route("/api/orders")
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Orders ORDER BY Order_ID")
    rows = cur.fetchall()

    columns = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    return jsonify([
        dict(zip(columns, row))
        for row in rows
    ])


# Dashboard statistics
@app.route("/api/stats")
def get_stats():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            (SELECT COUNT(*) FROM Books),
            (SELECT COUNT(*) FROM Customers),
            (SELECT COUNT(*) FROM Orders),
            (SELECT COALESCE(SUM(Total_Amount), 0) FROM Orders)
    """)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "total_books": result[0],
        "total_customers": result[1],
        "total_orders": result[2],
        "total_revenue": float(result[3])
    })

# Sales by Genre
@app.route("/api/sales-by-genre")
def sales_by_genre():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT b.Genre, SUM(o.Quantity) AS total_sold
        FROM Books b
        JOIN Orders o ON b.Book_ID = o.Book_ID
        GROUP BY b.Genre
        ORDER BY total_sold DESC;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {
            "genre": row[0],
            "total_sold": int(row[1])
        }
        for row in rows
    ])


# Top 5 Books
@app.route("/api/top-books")
def top_books():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT b.Title, SUM(o.Quantity) AS total_sold
        FROM Books b
        JOIN Orders o ON b.Book_ID = o.Book_ID
        GROUP BY b.Book_ID, b.Title
        ORDER BY total_sold DESC
        LIMIT 5;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {
            "title": row[0],
            "total_sold": int(row[1])
        }
        for row in rows
    ])


# Top 5 Customers
@app.route("/api/top-customers")
def top_customers():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.Name, SUM(o.Total_Amount) AS total_spent
        FROM Customers c
        JOIN Orders o ON c.Customer_ID = o.Customer_ID
        GROUP BY c.Customer_ID, c.Name
        ORDER BY total_spent DESC
        LIMIT 5;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {
            "name": row[0],
            "total_spent": float(row[1])
        }
        for row in rows
    ])


# Remaining Stock
@app.route("/api/stock")
def stock():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            b.Title,
            b.Stock - COALESCE(SUM(o.Quantity), 0) AS remaining_stock
        FROM Books b
        LEFT JOIN Orders o ON b.Book_ID = o.Book_ID
        GROUP BY b.Book_ID, b.Title, b.Stock
        ORDER BY remaining_stock ASC;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {
            "title": row[0],
            "remaining_stock": int(row[1])
        }
        for row in rows
    ])

if __name__ == "__main__":
    app.run(debug=True)