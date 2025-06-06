import os
import shutil
from uuid import uuid4
from PIL import Image
from fastapi import UploadFile, HTTPException
from io import BytesIO

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_image(image: UploadFile, max_size: int = 500):
    # Validasi ekstensi
    ext = image.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File harus berupa gambar JPG, JPEG, atau PNG")

    try:
        img = Image.open(image.file)

        if img.format not in ["JPEG", "PNG"]:
            raise HTTPException(status_code=400, detail="File gambar tidak valid (harus JPG/PNG)")

        img.thumbnail((max_size, max_size))  # resize dengan menjaga rasio

        # Simpan ke buffer
        buffer = BytesIO()
        img.save(buffer, format=img.format)
        buffer.seek(0)

        # Simpan ke disk
        uuid = uuid4()
        filename = f"{uuid}.{ext}"
        image_path = os.path.join(UPLOAD_DIR, filename)

        with open(image_path, "wb") as f:
            shutil.copyfileobj(buffer, f)

        return image_path, uuid

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image error: {str(e)}")
