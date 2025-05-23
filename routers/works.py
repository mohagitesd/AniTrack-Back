from fastapi import APIRouter, HTTPException
from services.anilist import get_work_details
from fastapi import Depends
from sqlmodel import Session, select
from core.security import get_current_user
from core.database import get_session
from models.progress import Progress
from models.rating import Rating
from models.user import User
from sqlalchemy.sql import func
from services.anilist import search_works
import httpx


router = APIRouter(prefix="/works", tags=["works"])

@router.get("/all-works")
async def get_all_works(max_pages: int = 5):
    
    
    all_works = []
    

    query = """
    query ($page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        pageInfo {
          currentPage
          hasNextPage
        }
        media {
          id
          title {
            romaji
            english
          }
          type
          genres
          status
          averageScore
          coverImage {
            large
          }
        }
      }
    }
    """

    async with httpx.AsyncClient() as client:
        for page in range(1, max_pages + 1):
            variables = {"page": page, "perPage": 50}
            response = await client.post(
                "https://graphql.anilist.co",
                json={"query": query, "variables": variables}
            )

            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Erreur Anilist : {response.text}")

            data = response.json()
            media_items = data["data"]["Page"]["media"]
            all_works.extend(media_items)

            if not data["data"]["Page"]["pageInfo"]["hasNextPage"]:
                break

    return all_works

@router.get("/search")
async def search(
    search: str = None,
    type: str = None,
    genre: str = None,
    year: int = None,
    status: str = None
):
    try:
        results = await search_works(search, type, genre, status)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Anilist Search : {str(e)}")


@router.get("/{anilist_id}")
async def get_work(
    anilist_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    try:
        work_data = await get_work_details(anilist_id)

        # Vérifier si l’oeuvre est suivie par l'utilisateur
        progress = session.exec(
            select(Progress).where(
                Progress.user_id == user.id,
                Progress.work_id == str(anilist_id)
            )
        ).first()

        is_followed = progress is not None

        # moyenne des notes de l'oeuvre
        average_rating = session.exec(
            select(func.avg(Rating.rating)).where(
                Rating.work_id == str(anilist_id)
            )
        ).one()

        local_average_rating = round(average_rating, 2) if average_rating is not None else None


        # Vérifier si l'utilisateur a noté l'oeuvre
        rating = session.exec(
            select(Rating).where(
                Rating.user_id == user.id,
                Rating.work_id == str(anilist_id)
            )
        ).first()

        return {
            **work_data, ## Inclure toutes les données de l'oeuvre
            "is_followed": is_followed, 
            "user_rating": rating.rating if rating else None,
            "user_review": rating.review if rating else None,
            "local_average_rating": local_average_rating,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Anilist : {str(e)}")


