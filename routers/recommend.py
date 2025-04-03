from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.progress import Progress
from models.rating import Rating
from models.user import User
from core.security import get_current_user
from core.database import get_session
from services.anilist import get_work_details, search_works

router = APIRouter(prefix="/recommend", tags=["recommendations"])

@router.get("/")
async def get_recommendations(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Récupère les œuvres suivies ou bien notées
    progresses = session.exec(
        select(Progress).where(Progress.user_id == user.id)
    ).all()

    ratings = session.exec(
        select(Rating).where(Rating.user_id == user.id, Rating.rating >= 7)
    ).all()

    work_ids = list(set([p.work_id for p in progresses] + [r.work_id for r in ratings]))

    if not work_ids:
        raise HTTPException(status_code=404, detail="Pas encore assez d’œuvres pour recommander.")

    # Compte les genres
    genres_count = {}
    for wid in work_ids:
        try:
            work = await get_work_details(int(wid))
            for genre in work.get("genres", []):
                genres_count[genre] = genres_count.get(genre, 0) + 1
        except:
            pass  # ignore erreurs

    if not genres_count:
        raise HTTPException(status_code=404, detail="Aucun genre trouvé")

    # Top 3 genres
    top_genres = sorted(genres_count, key=genres_count.get, reverse=True)[:3]

    # Recherche des recommandations
    recommendations = await search_works(genre=top_genres[0])  # pour l’instant le genre principal

    return {
        "based_on": top_genres,
        "recommendations": recommendations
    }
