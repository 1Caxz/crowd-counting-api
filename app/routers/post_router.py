import mimetypes
from fastapi import APIRouter, HTTPException, Request, UploadFile, Depends, File, Form, Query
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services import post_service
from app.schemas.post_schema import PostUpdate, PostResponse
from app.utils.image_helper import save_image
from app.utils.predict_helper import predict_count, save_densitymap, save_heatmap

router = APIRouter(prefix="/posts", tags=["Posts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", response_model=PostResponse)
def create(title: str = Form(...), content: str = Form(...), image: UploadFile = File(None), request: Request = None, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    if user_id is None:
        raise HTTPException(
            status_code=401, detail="Unauthorized: user_id not found in request")

    image_path, filename = save_image(image)
    count, map = predict_count(image_path)
    density = save_densitymap(map, filename)
    heatmap_path = save_heatmap(density, filename, count)
    service = post_service.create_post(
        db, title, content, user_id, image_path, heatmap_path, count)
    return {
        "id": service.id,
        "user_id": service.user_id,
        "title": service.title,
        "content": service.content,
        "image": image_path,
        "heatmap": heatmap_path,
        "count": count
    }


@router.post("/update/{id}", response_model=PostResponse)
def update(id: int, data: PostUpdate, db: Session = Depends(get_db)):
    return post_service.update_post(db, id, data)


@router.post("/delete/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return post_service.delete_post(db, id)


@router.get("/list", response_model=list[PostResponse])
def read(page: int = Query(0, ge=0), db: Session = Depends(get_db)):
    return post_service.get_posts(db, 10, page)
