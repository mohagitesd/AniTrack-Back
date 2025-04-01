from pydantic import BaseModel, EmailStr
from datetime import datetime

# Données attendues lors de l'inscription
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Ce n’est pas le champ dans la BDD mais la donnée reçue

# Données retournées à l’utilisateur
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True  # Permet d’utiliser un objet SQLAlchemy comme retour
