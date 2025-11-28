from sqlalchemy import Column, Integer, String
from .database import Base

class Config(Base):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    folder = Column(String(255), nullable=False)
    s3_url = Column(String(500), nullable=False)
