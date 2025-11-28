from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Config
from .schemas import ConfigResponse
from .s3_client import s3, S3_BUCKET

router = APIRouter(prefix="/configs")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ConfigResponse)
async def upload_config(folder: str, file: UploadFile, db: Session = Depends(get_db)):
    key = f"{folder}/{file.filename}"

    # Upload ke S3
    s3.upload_fileobj(file.file, S3_BUCKET, key)

    s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"

    # Simpan metadata ke RDS
    config = Config(name=file.filename, folder=folder, s3_url=s3_url)
    db.add(config)
    db.commit()
    db.refresh(config)

    return config


@router.get("/", response_model=list[ConfigResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(Config).all()


@router.get("/{folder}", response_model=list[ConfigResponse])
def get_by_folder(folder: str, db: Session = Depends(get_db)):
    return db.query(Config).filter(Config.folder == folder).all()
