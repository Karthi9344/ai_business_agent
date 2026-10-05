from fastapi import FastAPI

from app.database.connection import engine, Base
from app.database import models
from app.api.businesses import router as business_router
from app.api.products import router as product_router
from app.api.customers import router as customer_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="AI Business Agent")


app.include_router(business_router)
app.include_router(product_router)
app.include_router(customer_router)


@app.get("/")
def home():
    return {
        "message": "AI Business Agent API is running"
    }