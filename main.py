from core.database import engine
from sqlmodel import SQLModel
from fastapi import FastAPI
from models.user import User
from routers import auth ,progress,rating, works, recommend
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # autorise Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(progress.router)
app.include_router(rating.router)
app.include_router(works.router)
app.include_router(recommend.router)    

# Crée les tables automatiquement au lancement
SQLModel.metadata.create_all(engine)

# Crée toutes les tables automatiquement au démarrage
SQLModel.metadata.create_all(engine)
