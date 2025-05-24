from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hola Jota, soy JAFL desde la web 😎"}
