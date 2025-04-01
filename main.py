from core.database import engine
from sqlmodel import SQLModel
from fastapi import FastAPI
from models.user import User
from routers import auth  # si tu as bien un fichier routers/auth.py

app = FastAPI()

app.include_router(auth.router)

# Crée les tables automatiquement au lancement
SQLModel.metadata.create_all(engine)

# Crée toutes les tables automatiquement au démarrage
SQLModel.metadata.create_all(engine)
