
from .database import Base
from sqlalchemy import TIME, Column, String, Integer, DATETIME, Float, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(30))
    balance = Column(Integer)

class Wallet(Base):
    __tablename__ = "wallet"

    wallet_id = Column(Integer, primary_key=True)
 

class Station(Base):
    __tablename__ = "station"
    
    station_id = Column(Integer, primary_key=True)
    station_name = Column(String(30))
    longitude = Column(Float)
    latitude = Column(Float)

    station = relationship('Stop', back_populates='stop')

class Stop(Base):
    __tablename__ = "stop"
    
    stop_id = Column(Float, primary_key=True, autoincrement=True)
    arival_time = Column(String(30))
    departure_time = Column(String(30))
    fare = Column(Integer)

    train_id = Column(Integer, ForeignKey('train.train_id'))

    station_id = Column(Integer, ForeignKey('station.station_id'))

    stop = relationship('Station', back_populates='station')
    st = relationship('Train', back_populates='tr')


class Train(Base):
    __tablename__ = "train"

    train_id = Column(Integer, primary_key=True)
    train_name = Column(String(30))
    capacity = Column(Integer)

    tr = relationship('Stop', back_populates='st')


class Ticket(Base):
    __tablename__ = "ticket"
    ticket_id = Column(Integer, primary_key=True)
    time_after = Column(String(30))
    station_from = Column(Integer)
    statioin_to = Column(Integer)
    