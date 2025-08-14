from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Manufacturing Backend API is running!"}

@app.post("/products/")
def create_product(name: str, category: str, price: float, db: Session = Depends(get_db)):
    new_product = models.Product(name=name, category=category, price=price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()
