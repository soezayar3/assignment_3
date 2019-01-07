import json
from sqlalchemy import Table, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *

engine = create_engine('sqlite:///records.db')
Base = declarative_base()

with open('records.json', 'r') as f:
    candidates = json.load(f)

class Records(Base):
    __tablename__ = "candidate_records"
    UserId = Column(Integer, primary_key=True)
    constituency = Column(String)
    parliament = Column(String)
    year = Column(String)
    party = Column(String)
    ethnicity = Column(String)
    gender = Column(String)
    age = Column(Integer)
    name = Column(String)
    religion = Column(String)

Records.__table__.create(bind=engine, checkfirst=True)

records = []
for i, result in enumerate(candidates):
    row = {}
    row['UserId'] = i
    row['constituency'] = result['constituency']
    row['parliament'] = result['parliament']
    row['year'] = result['year']
    row['party'] = result['party']
    row['ethnicity'] = result['candidate']['ethnicity']
    row['gender'] = result['candidate']['gender']
    row['age'] = result['candidate']['age']
    row['name'] = result['candidate']['name']
    row['religion'] = result['candidate']['religion']
    records.append(row)

Session = sessionmaker(bind=engine)
session = Session() 

for record in records:
    row = Records(**record)
    #print(record)
    session.add(row)
session.commit()
