from sqlalchemy.orm import relationship

from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    address = Column(String)
    groups = relationship("Groups", back_populates="employee")


class Kids(Base):
    __tablename__ = 'kids'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    date_of_enrollment = Column(String)
    gender = Column(String)
    groups = relationship("Groups", back_populates="kid")


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    employee = relationship("Employees", back_populates="groups")
    kids_id = Column(Integer, ForeignKey("kids.id"))
    kid = relationship("Kids", back_populates='groups')
