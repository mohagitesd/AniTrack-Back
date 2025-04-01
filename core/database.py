from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,Session
from dotenv import load_dotenv
import os


# charge l'environnement depuis le fichier .env
load_dotenv()

# Récupère l'URL de la base de données depuis les variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL")

# Crée une instance de moteur SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) 
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()