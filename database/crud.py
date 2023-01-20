from typing import Type

import fastapi as fa
from sqlalchemy.orm import Session

from database import Base


def get(session: Session, Model: Type[Base], **kwargs) -> Base:
    return session.query(Model).filter_by(**kwargs).first()


def remove(session: Session, Model: Type[Base], id: int) -> None:
    model_obj = session.query(Model).get(id)
    if model_obj is None:
        raise fa.HTTPException(status_code=404, detail=f"Trying to remove {Model} with id {id}, which is not found.")
    session.delete(model_obj)
    session.commit()