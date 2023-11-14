import os
import requests
import urllib.parse
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session
from flask_bcrypt import Bcrypt
import bcrypt
import requests
from flask_session import Session
import random 
import sqlite3


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



class shoes:
  def __init__(self, name, price, picture):
    self.name = name
    self.price = f"{price:,}"
    self.picture = picture


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