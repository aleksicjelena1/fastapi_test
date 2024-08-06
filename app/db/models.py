from app.db.database import Base
from sqlalchemy import Column, Integer, String


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    address = Column(String)


class Kids(Base):
    __tablename__ = 'kids'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    date_of_enrollment = Column(String)
    gender = Column(String)


