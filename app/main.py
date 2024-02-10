from fastapi import FastAPI, Depends, Response, status, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from typing import Optional
from sqlalchemy.sql import desc, asc, text
from .exceptions import UnicornException, UnicornBadException, UnicornTicketException
from time import time

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request:Request, exc:UnicornException):
    return JSONResponse(
        status_code=404,
        content={"message": exc.msg}
    )

@app.exception_handler(UnicornBadException)
async def unicorn_exception_handler(request:Request, exc:UnicornBadException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.msg}
    )
@app.exception_handler(UnicornTicketException)
async def unicorn_exception_handler(request:Request, exc:UnicornTicketException):
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.msg}
    )
@app.post("/api/users/", response_model=schemas.UserSchema)
def create_user(response:Response, payload:schemas.UserSchema, db:Session=Depends(get_db)):
    user =  crud.create_user(payload=payload, db=db)
    if user:
        response.status_code = status.HTTP_201_CREATED
        
    return user


@app.post("/api/stations", response_model=schemas.StationSchema, status_code=status.HTTP_201_CREATED)
def creat_station(station:schemas.StationSchema, db:Session=Depends(get_db)):
    db_station = models.Station(
        station_id = station.station_id,
        station_name = station.station_name,
        longitude = station.longitude,
        latitude = station.latitude
    )
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station



@app.post("/api/trains", response_model=schemas.TrainResponseSchema, status_code=status.HTTP_201_CREATED)
def create_train(payload:schemas.TrainSchema, db:Session = Depends(get_db)):
    train = models.Train(train_id=payload.train_id, train_name=payload.train_name, capacity=payload.capacity)
    
    db.add(train)
    db.commit()
    db.refresh(train)

    

    for item in payload.stop:
        stop = models.Stop(stop_id=time(), arival_time=item.arival_time, departure_time=item.departure_time, fare = item.fare, train_id=payload.train_id, station_id=item.station_id)
        db.add(stop)
        db.commit()
        db.refresh(stop)


    
    if len(payload.stop):
        dct = dict(train_id=payload.train_id, train_name=payload.train_name, capacity=payload.capacity, service_start=payload.stop[0].departure_time, service_ends=payload.stop[len(payload.stop)-1].arival_time, num_stations=len(payload.stop))

        return dct
    

@app.get("/api/stations", response_model=schemas.GetStationResModel, status_code=status.HTTP_200_OK)
def get_stations(db:Session=Depends(get_db)):
    return {"stations": db.query(models.Station).all()}


@app.get("/api/stations/{station_id}/trains")
def get_station_trains(station_id:int, db:Session = Depends(get_db)):
    st = db.query(models.Station).filter(models.Station.station_id == station_id).all()
    if len(st) == 0:
        raise UnicornException(msg=f"station with id: {station_id} was not found")
    


    re = {"station_id": station_id, "trains": []}
    
    res = db.execute(text(f"select train_id, arival_time, departure_time from stop where stop.station_id == {station_id}")).all()

    re['trains'] = [item._mapping for item in res]

    return re


@app.get("/api/wallets/{wallet_id}")
def get_wallet(wallet_id:int, db:Session = Depends(get_db)):
    wlt = db.query(models.Wallet).filter(models.Wallet.wallet_id == wallet_id).first()

    if wlt is None:
        raise UnicornException(msg=f"wallet with id: {wallet_id} was not found")
    
    usr = db.query(models.User).filter(models.User.user_id == wallet_id).first()
    
    return {"wallet_id": wallet_id, "balance": usr.balance, "wallet_user": {"user_id": usr.user_id, "user_name":usr.user_name}}

@app.put("/api/wallets/{wallet_id}")
def update_wallet(wallet_id:int, recharge:schemas.RechargeSchema, db:Session = Depends(get_db)):
    wlt = db.query(models.Wallet).filter(models.Wallet.wallet_id == wallet_id).first()

    if wlt is None:
        raise UnicornException(msg=f"wallet with id: {wallet_id} was not found")
    
    if recharge.recharge < 100 or recharge.recharge > 10000:
        raise UnicornBadException(msg=f"Invalid amound: {recharge.recharge}")
    
    usr = db.query(models.User).filter(models.User.user_id == wallet_id).first()

    usr.balance = usr.balance + recharge.recharge

    db.commit()
    db.refresh(usr)

    return {"wallet_id": wallet_id, "balance": usr.balance, "wallet_user": {"user_id": usr.user_id, "user_name":usr.user_name}}


@app.post("/api/tickets")
def create_ticket(payload:schemas.TicketSchema, db:Session=Depends(get_db)):
    fr = db.query(models.Station).filter(models.Station.station_id == payload.station_from).first()
    to = db.query(models.Station).filter(models.Station.station_id == payload.statioin_to).first()

    if (fr and to) is None:
        raise UnicornTicketException(403, f"no ticket available for station: {payload.station_from} to station: {payload.statioin_to}")

    