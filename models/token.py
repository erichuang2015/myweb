import time

from sqlalchemy import Column, Integer, String

from models.base_model import SQLMixin, db


class Token(SQLMixin, db.Model):
    csrf_token = Column(String(36), nullable=False)
    user_id = Column(Integer, nullable=False)

    @classmethod
    def pop_exist(cls, user_id):
        try:
            old_token = Token.one(user_id=user_id)
            Token.delete(id=old_token.id)
        except:
            return