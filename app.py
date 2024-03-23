from flask import Flask

app = Flask(__name__)

paintInventory = [
    {
        "color": "blue",
        "quantity": 10,
        "paintStatus": "available"
    }
]

@app.get("/paint")
def get_paint_inventory():
    return {"paintInventory": paintInventory}