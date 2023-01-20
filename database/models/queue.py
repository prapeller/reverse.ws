import sqlalchemy as sa

from database import Base


class QueueModel(Base):
    __tablename__ = 'queue'

    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.String)

    def __repr__(self):
        return f"<QueueModel> ({self.id=:}, {self.full_name=:})"
