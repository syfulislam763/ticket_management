from pydantic import BaseModel
from typing import List




class UserSchema(BaseModel):
    user_id:int
    user_name:str
    balance:int
    class Config:
        orm_mode = True



class StopSchemaTable(BaseModel):
    stop_id:int
    train_id:int
    station_id:int 
    arival_time:str
    departure_time:str
    fare:int

    class Config:
        orm_mode = True

class StationSchema(BaseModel):
    station_id:int
    station_name:str
    longitude:float
    latitude:float

    class Config:
        orm_mode = True

class StopSchema(BaseModel):
    station_id:int 
    arival_time:str | None
    departure_time:str | None
    fare:int

    class Config:
        orm_mode = True

class TrainSchema(BaseModel):
    train_id:int
    train_name:str
    capacity: int
    stop: list[StopSchema]

    class Config:
        orm_mode = True


class TrainResponseSchema(BaseModel):
    train_id:int
    train_name:str
    capacity:int
    service_start:str
    service_ends:str
    num_stations:int


    class Config:
        orm_mode = True


class GetStationResModel(BaseModel):
    stations: list[StationSchema]

    class Config:
        orm_mode = True


class RechargeSchema(BaseModel):
    recharge:int

class TicketSchema(BaseModel):
    wallet_id:int
    time_after:str
    station_from:int
    statioin_to:int

    class Config:
        orm_mode = True
    