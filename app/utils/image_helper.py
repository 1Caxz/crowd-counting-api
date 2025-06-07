import os
import shutil
from uuid import uuid4
from PIL import Image
from fastapi import UploadFile, HTTPException
from io import BytesIO

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(image: UploadFile, max_size: int = 1024):
    ext = image.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Image extension invalid.")
    try:
        img = Image.open(image.file).convert("RGB")
        img.thumbnail((max_size, max_size))  # PENTING: resize eksplisit ke 224x224

        buffer = BytesIO()
        img.save(buffer, format="JPEG")  # simpan ulang sebagai JPEG
        buffer.seek(0)

        uuid = uuid4()
        filename = f"{uuid}.jpg"
        image_path = os.path.join(UPLOAD_DIR, filename)

        with open(image_path, "wb") as f:
            shutil.copyfileobj(buffer, f)

        return image_path, uuid

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image error: {str(e)}")
