from sqlalchemy import Column, Integer, String
from app.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(500), nullable=True)
    file_path = Column(String(255))

    # 🚀 Add these lines so your model matches what your database table wants:
    subject = Column(String(100), nullable=False, default="General")
    grade = Column(String(100), nullable=True, default="All Levels")
    type = Column(String(100), nullable=True, default="Notes")
    author = Column(String(255), nullable=True, default="Anonymous")