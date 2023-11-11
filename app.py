from flask import Flask, render_template
import random
app = Flask(__name__)


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
argon = shoes("argon", 1900, "https://fashfash.dk/cdn/shop/products/11_7c06be55-ce49-4aca-a4d7-e0ab26899afb.png?v=1667422746&width=535")
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

