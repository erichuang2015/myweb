import time

from sqlalchemy import String, Integer, Column, Text, UnicodeText, Unicode

from models.base_model import SQLMixin, db

class Todo(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    user_id = Column(Integer, nullable=False)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        t = cls.new(form)
        return t

    @classmethod
    def update(cls, _id, **kwargs):
        super().update(
            id=_id,
            title=kwargs['title']
        )

        t = Todo.one(id=_id)
        return t

    @property
    def serialize(self):
        """Return object data in easily serializeable format
        solve the problem "TypeError: Object of type 'InstanceState' is not JSON serializable "
        """
        return {
            'id': self.id,
            'title': self.title,
            'created_time': self.created_time,
            'updated_time': self.updated_time,
            'user_id': self.user_id
        }

    def json(self):
        return self.serialize



