from sqlalchemy import Column, DateTime, Integer, String
from database_connection import Base
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import relationship

class Stores(Base):
    __tablename__ = "Stores"
    Id = Column(String(36), primary_key=True)
    Name = Column(String(255), unique=True, index=True)

class Counts(Base):
    __tablename__ = "Counts"
    Id = Column(String(36), primary_key=True)
    StoreId = Column(String(36), index=True)
    ManCount = Column(Integer)
    WomanCount = Column(Integer)
    KidCount = Column(Integer)
    StaffCount = Column(Integer)
    EmployeeCount = Column(Integer)
    TotalCount = Column(Integer)
    CreatingDateTime = Column(DateTime, default=datetime.now(timezone.utc))
    UpdatingDateTime = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

