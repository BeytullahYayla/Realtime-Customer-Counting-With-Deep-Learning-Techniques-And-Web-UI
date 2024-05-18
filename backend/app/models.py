from pydantic import BaseModel
from datetime import date

class CountsGetResponse(BaseModel):
    ManCount : int
    WomanCount : int
    KidCount : int
    StaffCount : int
    EmployeeCount : int
    TotalCount : int
    DateTime : date

class CountsGetResponseByDateRange(BaseModel):
    ManCount : int
    WomanCount : int
    KidCount : int
    StaffCount : int
    EmployeeCount : int
    TotalCustomers : int
    TotalWorkers : int
    TotalCount : int
    DateTime : date

class StoresGetResponse(BaseModel):
    Name : str