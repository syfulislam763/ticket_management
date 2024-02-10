from sqlalchemy.orm import Session
from . import schemas, models

def create_user(payload:schemas.UserSchema, db:Session):
    user = models.User(user_id=payload.user_id, user_name=payload.user_name, balance=payload.balance)
    wlt = models.Wallet(wallet_id = payload.user_id)
    db.add(wlt)
    db.commit()
    db.refresh(wlt)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


