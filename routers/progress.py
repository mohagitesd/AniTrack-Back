from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.progress import Progress
from schemas.progress import ProgressCreate
from core.database import get_session
from core.security import get_current_user
from models.user import User
from services.anilist import get_work_details

router = APIRouter(prefix="/user", tags=["progress"])

@router.post("/progress")
def add_or_update_progress(data: ProgressCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    progress = session.exec(
        select(Progress).where(Progress.user_id == user.id, Progress.work_id == data.work_id)
    ).first()

    if progress:
        progress.status = data.status
        progress.current_episode = data.current_episode
        progress.current_chapter = data.current_chapter
    else:
        progress = Progress(
            user_id=user.id,
            **data.dict()
        )
        session.add(progress)

    session.commit()
    session.refresh(progress)
    return progress

@router.get("/progress")
def get_user_progress(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    progresses = session.exec(
        select(Progress).where(Progress.user_id == user.id)
    ).all()

    return progresses

@router.delete("/progress/{progress_id}")
def delete_progress(progress_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    progress = session.get(Progress, progress_id)

    if not progress or progress.user_id != user.id:
        raise HTTPException(status_code=404, detail="Progression introuvable ou non autorisée")

    session.delete(progress)
    session.commit()

    return {"message": "Progression supprimée avec succès"}

@router.get("/list")
async def list_followed_works(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    progresses = session.exec(
        select(Progress).where(Progress.user_id == user.id)
    ).all()

    results = []
    for progress in progresses:
        try:
            work_data = await get_work_details(int(progress.work_id))
        except Exception as e:
            work_data = {"error": f"Failed to fetch work {progress.work_id}"}
        
        results.append({
            "work_id": progress.work_id,
            "progress": progress.progress,
            "work": work_data
        })

    return results


