import flask_sqlalchemy


class BaseModel(flask_sqlalchemy.Model):
    __abstract__ = True

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()
