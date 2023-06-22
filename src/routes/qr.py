import qrcode
from starlette import status
import cloudinary
import cloudinary.uploader
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.database.models import Image, Qr
from io import BytesIO
from src.database.db import get_db
import os
from src.conf.config import settings, config_cloudinary

router = APIRouter(prefix='/qr', tags=["qr"])

# ------------------------------------------------------------???????????????????
# cloudinary.config(
#         cloud_name=settings.cloudinary_name,
#         api_key=settings.cloudinary_api_key,
#         api_secret=settings.cloudinary_api_secret,
#         secure=True
#     )
try:
    config_cloudinary()
#    upload_result = cloudinary.uploader.upload(qr_code_bytes, folder="qrs")
except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/generate_qr_code")
def generate_qr_code_and_upload_to_cloudinary(image_id, db: Session = Depends(get_db)):
    qr = db.query(Qr).filter(Qr.image_id == image_id).first()
    if qr:
        return {"qr_code_cloudinary_url": qr.qr_code_url}

    # Отримайте посилання на зображення
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="No image found with this ID")
    image_url = image.image

    # Створюємо QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(image_url)
    qr.make(fit=True)
    qr_code_image = qr.make_image(fill_color="black", back_color="white")

    # Зберігаємо QR-код у форматі BytesIO
    qr_code_bytes = BytesIO()
    qr_code_image.save(qr_code_bytes, format='png')
    qr_code_bytes.seek(0)

    # Завантажуємо QR-код на Cloudinary

    upload_result = cloudinary.uploader.upload(qr_code_bytes, folder="qrs")

    # Отримуємо URL зображення на Cloudinary
    qr_code_cloudinary_url = upload_result['secure_url']

    # Зберігаємо URL у базі даних
    qr_data = Qr(qr_code_url=qr_code_cloudinary_url, image_id=image_id)
    db.add(qr_data)
    db.commit()
    db.refresh(qr_data)

    return {"qr_code_cloudinary_url": qr_code_cloudinary_url}

@router.get("/")
def get_all_qr_codes(db: Session = Depends(get_db)):
    qr_codes = db.query(Qr).all()
    return {"qr_codes": qr_codes}

@router.put("/{qr_id}/update")
def update_qr_code(qr_id: int, db: Session = Depends(get_db)):
    print(qr_id)
    # Отримати QR-код за його ID
    qr = db.query(Qr).filter(Qr.id == qr_id).first()
    print(qr)
    if not qr:
        raise HTTPException(status_code=404, detail="QR code not found with the given ID.")

    # Отримайте посилання на зображення
    image = db.query(Image).filter(Image.id == Qr.image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="No image found with this ID")
    image_url = image.image

    # Створити новий QR-код
    qr_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr_code.add_data(image_url)
    qr_code.make(fit=True)
    qr_code_image = qr_code.make_image(fill_color="black", back_color="white")

    # Зберегти новий QR-код у форматі BytesIO
    qr_code_bytes = BytesIO()
    qr_code_image.save(qr_code_bytes, format='png')
    qr_code_bytes.seek(0)

    # Завантажуємо новий QR-код на Cloudinary

    upload_result = cloudinary.uploader.upload(qr_code_bytes, folder="qrs")

    # Видалення попереднього qr_code_url
    if qr.qr_code_url:
        separator = '/'
        parts = qr.qr_code_url.split(separator)
        public_id_with_extension = separator.join(parts[-2:])
        public_id = os.path.splitext(public_id_with_extension)[0]
        cloudinary.uploader.destroy(public_id, invalidate=True)


    # Оновлення URL QR-коду в базі даних
    qr.qr_code_url = upload_result['secure_url']
    db.commit()
    db.refresh(qr)

    return {"message": "QR code successfully updated.",
            "qr_code_cloudinary_url": qr.qr_code_url}

@router.delete("/{qr_id}/delete")
def delete_qr_code(qr_id: int, db: Session = Depends(get_db)):
    # Get the QR code by its ID
    qr = db.query(Qr).filter(Qr.id == qr_id).first()
    if not qr:
        raise HTTPException(status_code=404, detail="QR code not found with the given ID.")



    # Delete the QR code from Cloudinary
    if qr.qr_code_url:
        separator = '/'
        parts = qr.qr_code_url.split(separator)
        public_id_with_extension = separator.join(parts[-2:])
        public_id = os.path.splitext(public_id_with_extension)[0]
        cloudinary.uploader.destroy(public_id, invalidate=True)

    # Delete the QR code from the database
    db.delete(qr)
    db.commit()

    return {"message": "QR code successfully deleted."}




