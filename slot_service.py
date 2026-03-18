from sqlalchemy.orm import Session
from models import Slot
from schemas import SlotCreate, SlotUpdate

class SlotService:
    @staticmethod
    def create_slot(db: Session, slot: SlotCreate):
        db_slot = Slot(**slot.dict())
        db.add(db_slot)
        db.commit()
        db.refresh(db_slot)
        return db_slot

    @staticmethod
    def get_slots(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Slot).offset(skip).limit(limit).all()

    @staticmethod
    def get_slot(db: Session, slot_id: int):
        return db.query(Slot).filter(Slot.id == slot_id).first()

    @staticmethod
    def update_slot(db: Session, slot_id: int, slot_update: SlotUpdate):
        db_slot = db.query(Slot).filter(Slot.id == slot_id).first()
        if not db_slot:
            return None

        update_data = slot_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_slot, key, value)

        db.commit()
        db.refresh(db_slot)
        return db_slot

    @staticmethod
    def delete_slot(db: Session, slot_id: int):
        db_slot = db.query(Slot).filter(Slot.id == slot_id).first()
        if db_slot:
            db.delete(db_slot)
            db.commit()
            return True
        return False
