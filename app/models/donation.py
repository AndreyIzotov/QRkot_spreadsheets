from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.financial import Financial


class Donation(Base, Financial):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
