from fastapi import FastAPI

app = FastAPI(title="AI Business Agent")


@app.get("/")
def home():
    return {
        "message": "AI Business Agent API is running"
    }