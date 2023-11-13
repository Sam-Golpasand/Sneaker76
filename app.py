from flask import Flask, flash, redirect, render_template, request, session
from flask_bcrypt import Bcrypt
import bcrypt
import requests
from flask_session import Session
import random 
from sam import login_required
import sqlite3


app = Flask(__name__)
bcrypt = Bcrypt(app)
conn = sqlite3.connect("users.db")

c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price DECIMAL(10, 2) NOT NULL, picture TEXT, stock INTEGER NOT NULL, category TEXT);""")
c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL UNIQUE, passhash TEXT);""")
c.execute("""CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, status TEXT CHECK( status IN ('Pending','Completed','Cancelled') ) NOT NULL DEFAULT 'Pending', order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));""")
c.execute("""CREATE TABLE IF NOT EXISTS carts ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id)); """)
c.execute("""CREATE TABLE IF NOT EXISTS cart_items (id INTEGER PRIMARY KEY AUTOINCREMENT, cart_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (cart_id) REFERENCES carts(id), FOREIGN KEY (product_id) REFERENCES products(id));""")
conn.commit()
c.close()
conn.close()

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'my_secret_key'


Session(app)


@app.route("/")
def index():
  #global items
  #featured = items
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
    

  c.execute("SELECT * FROM products WHERE category='shoes'")
  featured_items = c.fetchall()

  featured = [{"id": row[0], "name": row[1], "price": row[2], "picture": row[3], "stock": row[4], "category": row[5]} for row in featured_items]

  c.close()
  conn.close()

  return render_template("index.html", featured=featured)




@app.route("/explore")
def explore():
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
    

  c.execute("SELECT * FROM products WHERE category='shoes'")
  featured_items = c.fetchall()

  items = [{"id": row[0], "name": row[1], "price": row[2], "picture": row[3], "stock": row[4], "category": row[5]} for row in featured_items]

  c.close()
  conn.close()


  return render_template("explore.html", items=items)



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")


        if not email:
            raise Exception("You must enter a email!")
        elif not password:
            raise Exception("You must enter a password!")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = c.fetchone()

        if row is None or not bcrypt.check_password_hash(row[2], password):
            raise Exception("Password does not match")
        
        session["user_id"] = int(row[0])
        conn.commit()

        return redirect("/")
    else:    
        return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
   if request.method == "POST":
      
      conn = sqlite3.connect("users.db")
      c = conn.cursor()

      email = request.form["email"]
      password = request.form["password"]
      confirm = request.form["confirm"]

      if not email:
          raise Exception("You must enter a email!")
      elif not password:
          raise Exception("You must enter a password!")
      elif not confirm:
          raise Exception("You must write confirmation password!")
      elif password != confirm:
          raise Exception("password and confirmation does not match")
      
      passhash = bcrypt.generate_password_hash(password).decode('utf-8')

      try:
        c.execute("INSERT INTO users (email, passhash) VALUES (?, ?)", (email, passhash))
        conn.commit()
        return redirect("/")
      except Exception as e: 
         print(e)
         return redirect("/")


   else:
    return render_template("register.html")




@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

@app.errorhandler(Exception)
def handle_error(error):
    return f"An error occurred: {str(error)}", 500




if __name__ == '__main__':
  app.run(debug=True)

