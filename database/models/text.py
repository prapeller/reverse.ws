import sqlalchemy as sa

from database import Base


class TextModel(Base):
    __tablename__ = 'text'

    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.String)

    def __repr__(self):
        return f"<TextModel> ({self.id=:}, {self.full_name=:})"
