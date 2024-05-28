from typing import Optional
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

class UsersGetResponse(BaseModel):
    Username : str
    Email : str
    Role : str
    IsEnable : str

class UserCreateRequest(BaseModel):
    Username : str
    Email : str
    Password : str
    SuperUser : Optional[bool] = False

class UserPatchRequest(BaseModel):
    Username : str
    Email : str
    
class UserLoginRequest(BaseModel):
    Email : str
    Password : str

class UserPasswordRequest(BaseModel):
    OldPassword : str
    NewPassword : str
