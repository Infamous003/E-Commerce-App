from fastapi import FastAPI
from .routes import auth, products, orders, cart
from .database import init_db

app = FastAPI(
    title="E-Commerce backend",
    summary="This is a backend for an E-Commerce Application. Built using FastAPI.")

app.include_router(products.router)
app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(cart.router)

try:
    init_db()
except Exception:
    print("Unable to connect to the database")

@app.get("/")
def root():
    return {"data": "Welcome to idk-what-to-call-this app. Enjoy ig...?"}