from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_bcrypt import Bcrypt
import requests
import random 
from sam import login_required
import sqlite3
import bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
conn = sqlite3.connect("users.db")

c = conn.cursor()



c.execute("""CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, price DECIMAL(10, 2) NOT NULL, picture TEXT, stock INTEGER NOT NULL, category TEXT);""")

c.execute("""CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL,last_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, phone TEXT, address TEXT, city TEXT, country TEXT);""")

c.execute("""CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, status TEXT CHECK( status IN ('Pending','Completed','Cancelled') ) NOT NULL DEFAULT 'Pending', order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));""")

c.execute("""
CREATE TABLE IF NOT EXISTS carts ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id)); """)

c.execute("""CREATE TABLE IF NOT EXISTS cart_items (id INTEGER PRIMARY KEY AUTOINCREMENT, cart_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (cart_id) REFERENCES carts(id), FOREIGN KEY (product_id) REFERENCES products(id));""")



conn.commit()
c.close()
conn.close()

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'my_secret_key'

Session(app)


@app.route("/")
def index():
  global items
  featured = items


  return render_template("index.html", featured=featured)


@app.route("/explore")
def explore():
  global items

  return render_template("explore.html", items=items)


@app.route("/redirect")
def redirect():
  return render_template("redirect.html")


class shoes:
  def __init__(self, name, price, picture):
    self.name = name
    self.price = f"{price:,}"
    self.picture = picture

retroWhite = shoes("Air Jordan 4 Retro White Midnight Navy", 200, "https://fashfash.dk/cdn/shop/products/et.png?v=1667423285&width=535")
varsityGreen = shoes("Nike Low Varsity Green", 3000, "https://fashfash.dk/cdn/shop/products/nike-dunk-low-team-green-1-1000.png?v=1642264764&width=535")
newBalance = shoes("New Balance", 700, "https://fashfash.dk/cdn/shop/files/1_9.webp?v=1689701425&width=535")
jordan4L = shoes("Air Jordan 4 Lightning", 2400, "https://fashfash.dk/cdn/shop/products/air-jordan-4-lightning-2021-1-1000.png?v=1642112879&width=535")
mcQueens = shoes("McQueens", 4000, "../static/img/mcqueens.png")
argon = shoes("Argon", 1900, "https://fashfash.dk/cdn/shop/products/11_7c06be55-ce49-4aca-a4d7-e0ab26899afb.png?v=1667422746&width=535")
patent = shoes("Air Jordan 1 High Patent Red", 2400, "https://fashfash.dk/cdn/shop/products/image_d4135388-05e8-4825-aa99-253d3aeadbe0.png?v=1646264833&width=535")
roseWhisper = shoes("Nike Dunk Low Rose Whisper", 1600, "https://fashfash.dk/cdn/shop/files/1_6.webp?v=1688998550&width=535")
pineGreen = shoes("Air Jordan 4 Retro Pine Green", 3850, "https://fashfash.dk/cdn/shop/files/1_3.webp?v=1688569809&width=535")
lotteryPack = shoes("Nike Dunk Low Lottery Pack Grey Fog", 2400, "https://fashfash.dk/cdn/shop/files/1_2.webp?v=1688569102&width=535")
slideBone = shoes("Yeezy Slide Bone", 1300, "https://fashfash.dk/cdn/shop/products/yeezy-slide-pure-1-1000.png?v=1642199378&width=535")
airForce1 = shoes('Air Force 1 "White"', 1050, "https://fashfash.dk/cdn/shop/products/nike-air-force-1-low-white-07-1-1000.png?v=1642118600&width=535")
whiteOreo = shoes("Jordan 4 White Oreo", 4500, "https://fashfash.dk/cdn/shop/products/air-jordan-4-retro-white-oreo-2021-1-1000.png?v=1642113668&width=535")

items = [newBalance, jordan4L, varsityGreen, mcQueens, retroWhite, argon, patent, roseWhisper, pineGreen, lotteryPack, slideBone, airForce1, whiteOreo]


if __name__ == '__main__':
  app.run(debug=True)

