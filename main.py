from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from routers import auth

app = FastAPI()

app.include_router(auth.router)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Connexion a supabase reussie"}