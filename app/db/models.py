from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    address = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship("Groups", back_populates="employees")


class Kids(Base):
    __tablename__ = 'kids'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    date_of_enrollment = Column(String)
    gender = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship("Groups", back_populates="kids")


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    employees = relationship("Employees", back_populates="group")
    kids = relationship("Kids", back_populates='group')


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
