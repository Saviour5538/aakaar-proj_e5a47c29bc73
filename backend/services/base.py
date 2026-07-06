from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

T = TypeVar("T")  # SQLAlchemy model type

class CRUDService(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, db: Session, obj_in: dict) -> T:
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Integrity error: " + str(e))

    def read(self, db: Session, id: str) -> Optional[T]:
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, db: Session, id: str, obj_in: dict) -> T:
        db_obj = self.read(db, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: str) -> None:
        db_obj = self.read(db, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        db.delete(db_obj)
        db.commit()

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        return db.query(self.model).offset(skip).limit(limit).all()