from fastapi import FastAPI

app = FastAPI(
    title="E-Commerce backend",
    summary="This is a backend for an E-Commerce Application. Built using FastAPI.")

@app.get("/")
def root():
    return {"data": "Welcome to idk-what-to-call-this app. Enjoy ig...?"}