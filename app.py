from flask import Flask, redirect, render_template, request, session, flash, url_for
from flask_bcrypt import Bcrypt
import bcrypt
from decimal import Decimal
from flask_session import Session
import os
from sam import login_required, dbCon, dbClose
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

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
            flash("Email and password required", "warning")

        conn, c = dbCon()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = c.fetchone()

        if row is None or not bcrypt.check_password_hash(row["passhash"], password):
            dbClose(conn, c)
            flash("Invalid email or password", "warning")
            return redirect("/login")
        
        
        session["user_id"] = row["id"]
        dbClose(conn, c)
        flash("You have been logged in!", "info")
        return redirect("/")
    else:    
        return render_template("login.html")

def ensure_cart_exists(user_id):
    conn, c = dbCon()
    c.execute("SELECT id FROM carts WHERE user_id = ?", (user_id,))
    cart = c.fetchone()
    if not cart:
        c.execute("INSERT INTO carts (user_id) VALUES (?)", (user_id,))
        conn.commit()
        cart_id = c.lastrowid  # This gets the new cart's ID after the insert
    else:
        cart_id = cart['id']  # Access the ID using the column name as the key
    dbClose(conn, c)
    return cart_id



@app.route("/update-cart-item/<int:item_id>", methods=["POST"])
@login_required
def update_cart_item(item_id):
    user_id = session.get("user_id")
    new_quantity = request.form.get('quantity', type=int)

    if new_quantity is None or new_quantity < 1:
        flash("Invalid quantity specified", "danger")
        return redirect("/cart")

    conn, c = dbCon()
    c.execute("SELECT id FROM cart_items WHERE product_id = ? AND cart_id = (SELECT id FROM carts WHERE user_id = ?)", (item_id, user_id))
    cart_item = c.fetchone()

    if cart_item:
        c.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (new_quantity, cart_item['id']))
        conn.commit()
        flash("Cart updated successfully", "success")
    else:
        flash("Item not found in cart", "danger")

    dbClose(conn)
    return redirect("/cart")




@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    user_id = session.get("user_id")
    cart_id = ensure_cart_exists(user_id)
    
    conn, c = dbCon()
    c.execute("""
        SELECT id, quantity FROM cart_items
        WHERE cart_id = ?
        AND product_id = ?
    """, (cart_id, product_id))
    
    item = c.fetchone()
    if item:
        c.execute("UPDATE cart_items SET quantity = quantity + 1 WHERE id = ?", (item['id'],))
    else:
        c.execute("INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (?, ?, 1)", (cart_id, product_id))
    conn.commit()
    dbClose(conn)
    
    flash("Item added to cart", "success")
    return redirect("/cart")

@app.route("/remove-from-cart/<int:cart_item_id>", methods=["POST"])
@login_required
def remove_from_cart(cart_item_id):
    user_id = session.get("user_id")
    conn, c = dbCon()
    c.execute("SELECT id FROM carts WHERE user_id = ?", (user_id,))
    cart = c.fetchone()

    if cart:
        c.execute("""
            DELETE FROM cart_items
            WHERE product_id = ? AND cart_id = ?
        """, (cart_item_id, cart['id']))
        conn.commit()

    dbClose(conn)

    flash("Item removed from cart", "success")
    return redirect('/cart')

@app.route("/cart")
@login_required
def cart():
    user_id = session.get("user_id")
    conn, c = dbCon()
    c.execute("""
        SELECT 
            p.id,  
            p.name, 
            p.price, 
            p.picture,
            ci.quantity
        FROM 
            cart_items ci
            JOIN products p ON ci.product_id = p.id
        WHERE 
            ci.cart_id = (SELECT id FROM carts WHERE user_id = ?)
    """, (user_id,))
    cart_items = c.fetchall()
    total_price = 0  # Initialize total price

    new_cart_items = []  # Create a new list to hold modified cart items
    for item in cart_items:
        new_item = dict(item)  # Convert the sqlite3.Row object to a dictionary
        new_item['price'] = int(new_item['price'].replace(',', ''))  # Ensure price is a float
        item_total = new_item['price'] * new_item['quantity']  # Calculate total for this item
        total_price += item_total  # Accumulate to grand total
        new_cart_items.append(new_item)

    dbClose(conn)
    return render_template("cart.html", cart_items=new_cart_items, total_price=total_price)


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


        c.execute("INSERT INTO users (email, passhash) VALUES (?, ?)", (email, passhash))
        conn.commit()

        dbClose(conn, c)
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out!", "info")
    return redirect("/")

@app.errorhandler(Exception)
def handle_error(error):
    return f"An error occurred: {str(error)}", 500

if __name__ == '__main__':
    app.run(debug=True)
