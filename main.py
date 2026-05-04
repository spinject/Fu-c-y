import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from config import BOT_TOKEN, ADMIN_ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Load DB
def load():
    with open("database.json","r") as f:
        return json.load(f)

def save(data):
    with open("database.json","w") as f:
        json.dump(data,f,indent=4)

# START
@dp.message(Command("start"))
async def start(msg: types.Message):
    db = load()
    uid = str(msg.from_user.id)

    if uid not in db["users"]:
        db["users"][uid] = {"balance":0}
        save(db)

    await msg.answer("🛍 Welcome to Ultra Shop Bot\nUse /shop to buy products")

# SHOP
@dp.message(Command("shop"))
async def shop(msg: types.Message):
    db = load()
    text = "🛒 PRODUCTS:\n\n"

    for pid, p in db["products"].items():
        text += f"{pid}. {p['name']} - {p['price']}৳\n"

    await msg.answer(text)

# BUY
@dp.message(Command("buy"))
async def buy(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.answer("Usage: /buy product_id")

    pid = args[1]
    db = load()
    uid = str(msg.from_user.id)

    if pid not in db["products"]:
        return await msg.answer("❌ Invalid product")

    product = db["products"][pid]

    order_id = str(len(db["orders"]) + 1)
    db["orders"][order_id] = {
        "user": uid,
        "product": product["name"],
        "status": "pending"
    }

    save(db)

    await msg.answer(
        f"✅ Order Created\n\nProduct: {product['name']}\nPrice: {product['price']}৳\n\n💳 Pay via bKash/Nagad/Rocket"
    )

# ADMIN ADD PRODUCT
@dp.message(Command("add"))
async def add(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    args = msg.text.split("|")
    if len(args) < 3:
        return await msg.answer("Format: /add|name|price")

    db = load()
    pid = str(len(db["products"]) + 1)

    db["products"][pid] = {
        "name": args[1],
        "price": args[2]
    }

    save(db)
    await msg.answer("✅ Product added")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
