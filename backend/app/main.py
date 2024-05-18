from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, ValidationError
from datetime import datetime, timedelta
from typing import List
import tables
from models import CountsGetResponse, StoresGetResponse, CountsGetResponseByDateRange
from database_connection import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/stores", response_model=List[StoresGetResponse])
def get_stores():
    try:
        db = SessionLocal()

        query = text("SELECT Name from Stores ORDER BY Name")
        result = db.execute(query)
        stores = []
        for row in result.fetchall():
            row_dict = row._asdict()
            stores.append(StoresGetResponse(**row_dict))
        return stores
    except Exception as e:
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

@app.get("/stores/{store_name}/counts", response_model=List[CountsGetResponse])
def get_counts_by_store_name(store_name: str):
    try:
        db = SessionLocal()

        store_query = text("SELECT Id FROM Stores WHERE Name = :name")
        store_result = db.execute(store_query, {"name": store_name})
        store = store_result.fetchone()
        if not store:
            raise HTTPException(status_code=404, detail="Store not found")

        store_id = store[0]

        counts_query = text("SELECT ManCount, WomanCount, KidCount, StaffCount, EmployeeCount, TotalCount, DATE_FORMAT(UpdatingDateTime, '%Y-%m-%d') AS DateTime FROM Counts WHERE StoreId = :store_id ORDER BY UpdatingDateTime")
        counts_result = db.execute(counts_query, {"store_id": store_id})
        counts = []
        for row in counts_result.fetchall():
            row_dict = row._asdict()
            row_dict['DateTime'] = datetime.strptime(row_dict['DateTime'], '%Y-%m-%d').strftime('%Y-%m-%d')
            counts.append(CountsGetResponse(**row_dict))
        
        return counts
    except Exception as e:
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    
@app.get("/stores/{store_name}/counts/{date_range}", response_model=List[CountsGetResponseByDateRange])
def get_counts_by_store_name(store_name: str, date_range: str):
    try:
        db = SessionLocal()

        store_query = text("SELECT Id FROM Stores WHERE Name = :name")
        store_result = db.execute(store_query, {"name": store_name})
        store = store_result.fetchone()
        if not store:
            raise HTTPException(status_code=404, detail="Store not found")

        store_id = store[0]

        counts_query = text("SELECT ManCount, WomanCount, KidCount,StaffCount, EmployeeCount, (ManCount+WomanCount+KidCount) AS TotalCustomers, (StaffCount+EmployeeCount) AS TotalWorkers, TotalCount, DATE_FORMAT(UpdatingDateTime, '%Y-%m-%d') AS DateTime FROM Counts WHERE StoreId = :store_id AND UpdatingDateTime >= NOW() - INTERVAL " + date_range  +" ORDER BY UpdatingDateTime")
        counts_result = db.execute(counts_query, {"store_id": store_id})
        counts = []
        for row in counts_result.fetchall():
            row_dict = row._asdict()
            row_dict['DateTime'] = datetime.strptime(row_dict['DateTime'], '%Y-%m-%d').strftime('%Y-%m-%d')
            counts.append(CountsGetResponseByDateRange(**row_dict))
        
        return counts
    except Exception as e:
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
