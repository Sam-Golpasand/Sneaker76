from flask import Flask, redirect, render_template, request, session
from flask_bcrypt import Bcrypt
import bcrypt
from flask_session import Session
from sam import login_required, dbCon, dbClose
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'my_secret_key'  # Replace with a strong secret, possibly from os.urandom(24)

Session(app)

@app.route("/")
def index():
    conn, c = dbCon()
    c.execute("SELECT * FROM products WHERE category='shoes'")
    featured_items = c.fetchall()
    featured = [{"id": row["id"], "name": row["name"], "price": row["price"], "picture": row["picture"], "stock": row["stock"], "category": row["category"]} for row in featured_items]
    dbClose(conn, c)
    return render_template("index.html", featured=featured)

@app.route("/explore")
def explore():
    conn, c = dbCon()
    c.execute("SELECT * FROM products WHERE category='shoes'")
    items = c.fetchall()
    dbClose(conn, c)
    return render_template("explore.html", items=items)

@app.route("/shoe/<int:shoe_id>")
def shoe_detail(shoe_id):
    conn, c = dbCon()
    c.execute("SELECT * FROM products WHERE id = ?", (shoe_id,))
    shoe = c.fetchone()
    if shoe is None:
        dbClose(conn, c)
        return "Shoe not found", 404
    shoe_detail = {"id": shoe["id"], "name": shoe["name"], "price": shoe["price"], "picture": shoe["picture"], "stock": shoe["stock"], "category": shoe["category"]}
    dbClose(conn, c)
    return render_template("shoe_detail.html", shoe=shoe_detail)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Email and password required", 400

        conn, c = dbCon()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = c.fetchone()

        if row is None or not bcrypt.check_password_hash(row["passhash"], password):
            dbClose(conn, c)
            return "Invalid email or password", 401
        
        session["user_id"] = row["id"]
        dbClose(conn, c)
        return redirect("/")
    else:    
        return render_template("login.html")

@app.route("/cart")
@login_required 
def cart():
    conn, c = dbCon()
    c.execute("SELECT * FROM cart WHERE user_id = ?", (session["user_id"],))
    row = c.fetchone()
    dbClose(conn, c)
    # More logic here as needed
    return render_template("cart.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if not all([email, password, confirm]):
            return "All fields are required", 400
        if password != confirm:
            return "Passwords do not match", 400

        conn, c = dbCon()
        passhash = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            c.execute("INSERT INTO users (email, passhash) VALUES (?, ?)", (email, passhash))
            conn.commit()
        except sqlite3.IntegrityError:
            dbClose(conn, c)
            return "Email already registered", 400

        dbClose(conn, c)
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.errorhandler(Exception)
def handle_error(error):
    return f"An error occurred: {str(error)}", 500

if __name__ == '__main__':
    app.run(debug=True)
