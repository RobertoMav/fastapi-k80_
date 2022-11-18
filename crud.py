from sqlalchemy.orm import Session

import models, schemas

def get_data(db: Session, image_name: str):
    return db.query(models.Data).filter(models.Data.image == image_name).first()

def get_all_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Data).offset(skip).limit(limit).all()

def get_data_id(db: Session, id: int):
    return db.query(models.Data).filter(models.Data.id == id).first()

def create_data(db: Session, data: schemas.DataCreate):
    db_data = models.Data(image=data.image, output=data.output)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def delete_data(db: Session, data: schemas.DataDelete):
    db_data = get_data_id(db, data.id_deleted)
    image = db_data.image
    db.delete(db_data)
    db.commit()
    return {"deleted image name": image}


def delete_data_all(db: Session, skip: int = 0, limit: int = 500):
    db_data = get_all_data(db, skip, limit)
    for i in range(len(db_data)):
        db.delete(db_data[i])
        db.commit()
    return {"deleted ALL, you're crazy!!"}
