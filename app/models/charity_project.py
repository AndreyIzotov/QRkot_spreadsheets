from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.financial import Financial


class CharityProject(Base, Financial):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
