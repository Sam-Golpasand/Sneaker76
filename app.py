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
      except Exception as e: print(e)

   else:
    return render_template("register.html")





class shoes:
  def __init__(self, name, price, picture):
    self.name = name
    self.price = f"{price:,}"
    self.picture = picture


@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

@app.errorhandler(Exception)
def handle_error(error):
    return f"An error occurred: {str(error)}", 500

import time

def insert_shoes_into_db(shoe_list):
    # Open a new database connection each time this function is called
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    for shoe in shoe_list:
        # Prepare an SQL statement to insert shoe data
        c.execute("INSERT INTO products (name, price, picture, stock, category) VALUES (?, ?, ?, ?, ?)",
                  (shoe.name, shoe.price, shoe.picture, random.randint(0, 10), "shoes"))  

    conn.commit()
    c.close()
    conn.close()



retroWhite = shoes("Air Jordan 4 Retro White Midnight Navy", 2800, "https://fashfash.dk/cdn/shop/products/et.png?v=1667423285&width=535")
varsityGreen = shoes("Nike Low Varsity Green", 3000, "https://fashfash.dk/cdn/shop/products/nike-dunk-low-team-green-1-1000.png?v=1642264764&width=535")
newBalance = shoes("New Balance 2002R Nightwatch Green", 2000, "https://fashfash.dk/cdn/shop/products/n.png?v=1667424401&width=360")
jordan4L = shoes("Air Jordan 4 Lightning", 2400, "https://fashfash.dk/cdn/shop/products/air-jordan-4-lightning-2021-1-1000.png?v=1642112879&width=535")
mcQueens = shoes("Jordan 4 Retro SE Black Canvas", 3750, "https://fashfash.dk/cdn/shop/products/air-jordan-4-retro-se-black-canvas-1-1000.png?v=1671655654&width=360")
argon = shoes("Nike Dunk Low Argon", 1900, "https://fashfash.dk/cdn/shop/products/11_7c06be55-ce49-4aca-a4d7-e0ab26899afb.png?v=1667422746&width=535")
patent = shoes("Air Jordan 1 High Patent Red", 2400, "https://fashfash.dk/cdn/shop/products/image_d4135388-05e8-4825-aa99-253d3aeadbe0.png?v=1646264833&width=535")
roseWhisper = shoes("Nike Dunk Low Rose Whisper", 1600, "https://fashfash.dk/cdn/shop/files/1_6.webp?v=1688998550&width=535")
pineGreen = shoes("Air Jordan 4 Retro Pine Green", 3850, "https://fashfash.dk/cdn/shop/files/1_3.webp?v=1688569809&width=535")
lotteryPack = shoes("Nike Dunk Low Lottery Pack Grey Fog", 2400, "https://fashfash.dk/cdn/shop/files/1_2.webp?v=1688569102&width=535")
slideBone = shoes("Yeezy Slide Bone", 1300, "https://fashfash.dk/cdn/shop/products/yeezy-slide-pure-1-1000.png?v=1642199378&width=535")
airForce1 = shoes('Air Force 1 "White"', 1050, "https://fashfash.dk/cdn/shop/products/nike-air-force-1-low-white-07-1-1000.png?v=1642118600&width=535")
whiteOreo = shoes("Jordan 4 White Oreo", 4500, "https://fashfash.dk/cdn/shop/products/air-jordan-4-retro-white-oreo-2021-1-1000.png?v=1642113668&width=535")

items = [newBalance, jordan4L, varsityGreen, mcQueens, retroWhite, argon, patent, roseWhisper, pineGreen, lotteryPack, slideBone, airForce1, whiteOreo]

#insert_shoes_into_db(items)

if __name__ == '__main__':
  app.run(debug=True)

