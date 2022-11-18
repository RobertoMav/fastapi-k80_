from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home_page():
    return {"health": "check"}


@app.post("/data/", response_model=schemas.Data)
def create_data(data: schemas.DataCreate, db: Session = Depends(get_db)):
    data_check = crud.get_data(db, image_name=data.image)
    if data_check:
        raise HTTPException(status_code=400, detail="image already ran")
    return crud.create_data(db, data=data)


@app.get("/data/", response_model=list[schemas.Data])
def read_all_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_all_data(db, skip=skip, limit=limit)
    return data

@app.get("/data/{image_name}", response_model=schemas.Data)
def read_data(image_name: str, db: Session = Depends(get_db)):
    data = crud.get_data(db, image_name=image_name)
    if data is None:
        raise HTTPException(status_code=404, detail="Is this reality?")
    return data

@app.delete("/data/{id}")
def delete_data(data: schemas.DataDelete, db: Session = Depends(get_db)):
    data_check = crud.get_data_id(db, id=data.id_deleted)
    if data_check is None:
        raise HTTPException(status_code=404, detail="we are all quantum oscilations")
    return crud.delete_data(db, data=data)


@app.delete("/data/")
def DESTROY_EARTH(skip: int = 0, limit: int = 500, db: Session = Depends(get_db)):
    return crud.delete_data_all(db, skip=skip, limit=limit)
