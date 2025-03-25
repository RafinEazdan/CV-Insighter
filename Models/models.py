from Database.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

class CVs(Base):
    __tablename__ = 'cvs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    education = Column(JSONB, default=[])
    experience = Column(JSONB, default=[])
    skill = Column(JSONB, default=[])
    summary = Column(String)