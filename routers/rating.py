from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from core.database import get_session
from core.security import get_current_user
from models.rating import Rating
from models.user import User
from schemas.rating import RatingCreate

router = APIRouter(prefix="/user", tags=["rating"])

@router.post("/rating")
def rate_work(data: RatingCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    existing = session.exec(
        select(Rating).where(Rating.user_id == user.id, Rating.work_id == data.work_id)
    ).first()

    if existing:
        existing.rating = data.rating
        existing.review = data.review
    else:
        new_rating = Rating(user_id=user.id, **data.dict())
        session.add(new_rating)

    session.commit()
    return {"message": "Rating enregistré avec succès"}

@router.get("/rating")
def get_user_ratings(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    ratings = session.exec(
        select(Rating).where(Rating.user_id == user.id)
    ).all()

    return ratings
@router.put("/rating/{rating_id}")
def update_rating(
    rating_id: int,
    data: RatingCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    rating = session.get(Rating, rating_id)

    if not rating or rating.user_id != user.id:
        raise HTTPException(status_code=404, detail="Avis non trouvé ou non autorisé")

    rating.rating = data.rating
    rating.review = data.review

    session.commit()
    session.refresh(rating)
    return rating

@router.delete("/rating/{rating_id}")
def delete_rating(
    rating_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    rating = session.get(Rating, rating_id)

    if not rating or rating.user_id != user.id:
        raise HTTPException(status_code=404, detail="Avis non trouvé ou non autorisé")

    session.delete(rating)
    session.commit()

    return {"message": "Avis supprimé avec succès"}

