from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, ValidationError
from datetime import datetime, timedelta
from typing import List
from models import UserPasswordRequest,UserPatchRequest, UsersGetResponse, UserLoginRequest, UserCreateRequest, CountsGetResponse, StoresGetResponse, CountsGetResponseByDateRange
from database_connection import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
import secrets
from passlib.context import CryptContext

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data:dict):
    import jwt
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/register", response_model=dict)
async def create_user(user:UserCreateRequest):
    try:
        db = SessionLocal()

        user_check_query = text("SELECT Id FROM Users WHERE Email = :email OR Username = :username")
        user_check_result = db.execute(user_check_query, {"email": user.Email, "username": user.Username})
        existing_user = user_check_result.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        HashedPassword = pwd_context.hash(user.Password)

        insert_query = text("""
            INSERT INTO Users (Username, Email, Password, SuperUser) 
            VALUES (:username, :email, :password, :superuser)
        """)
        db.execute(insert_query, {
            "username": user.Username,
            "email": user.Email,
            "password": HashedPassword,
            "superuser":user.SuperUser
        })

        db.commit()

        return {"message": "User created successfully"}
    except HTTPException as http_exc:
        print("An error occurred:", http_exc)
        raise http_exc
    except Exception as e:
        db.rollback()
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    finally:
        db.close()

@app.post("/login", response_model=dict)
async def login(user:UserLoginRequest):
    try:
        db = SessionLocal()

        user_query = text("SELECT Id, Username, Email, Password, SuperUser, IsActive FROM Users WHERE Email = :email")
        user_result = db.execute(user_query, {"email": user.Email})
        existing_user = user_result.fetchone()
        print(existing_user)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_id, username, email, stored_password, super_user, is_active = existing_user

        if not is_active:
            raise HTTPException(status_code=403, detail="User is not active")

        if not pwd_context.verify(user.Password, stored_password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        role = "superuser" if super_user else "admin"
        user_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "role": role
        }
        access_token = create_access_token(user_data)

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as http_exc:
        print("An error occurred:", http_exc)
        raise http_exc
    except Exception as e:
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    finally:
        db.close()

@app.get("/users", response_model=List[UsersGetResponse])
def get_all_users():
    try:
        db = SessionLocal()
        
        users_query = text("SELECT Username, Email, SuperUser, IsActive FROM Users ORDER BY Username")
        users_result = db.execute(users_query)
        users = []
        for row in users_result.fetchall():
            role = "SuperUser" if row.SuperUser else "Admin"
            is_enable = "Enabled" if row.IsActive else "Disabled"
            user_response = UsersGetResponse(
                Username=row.Username,
                Email=row.Email,
                Role=role,
                IsEnable=is_enable
            )
            users.append(user_response)
        
        return users
    except Exception as e:
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    finally:
        db.close()

@app.patch("/users/{username}/toggle-activation", response_model=dict)
def toggle_user_activation(username: str):
    try:
        db = SessionLocal()

        user_check_query = text("SELECT Id, IsActive FROM Users WHERE Username = :username")
        user_check_result = db.execute(user_check_query, {"username": username})
        existing_user = user_check_result.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_id, is_active = existing_user

        new_status = not is_active
        update_query = text("UPDATE Users SET IsActive = :new_status WHERE Username = :username")
        db.execute(update_query, {"new_status": new_status, "username": username})
        db.commit()

        return {"message": f"User activation status changed to {new_status}"}
    except HTTPException as http_exc:
        print("An error occurred:", http_exc)
        raise http_exc
    except Exception as e:
        db.rollback()
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    finally:
        db.close()

@app.patch("/users/{username}/toggle-role", response_model=dict)
def toggle_user_role(username: str):
    try:
        db = SessionLocal()

        user_check_query = text("SELECT Id, SuperUser FROM Users WHERE Username = :username")
        user_check_result = db.execute(user_check_query, {"username": username})
        existing_user = user_check_result.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_id, super_user = existing_user

        new_role = not super_user
        update_query = text("UPDATE Users SET SuperUser = :new_role WHERE Username = :username")
        db.execute(update_query, {"new_role": new_role, "username": username})
        db.commit()

        role = "SuperUser" if new_role else "Admin"

        return {"message": f"User Role changed to {role}"}
    except HTTPException as http_exc:
        print("An error occurred:", http_exc)
        raise http_exc
    except Exception as e:
        db.rollback()
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    finally:
        db.close()

@app.patch("/users/{username}", response_model=dict)
def update_user(username: str, user_update: UserPatchRequest):
    try:
        db = SessionLocal()

        user_check_query = text("SELECT Id,SuperUser FROM Users WHERE Username = :username")
        user_check_result = db.execute(user_check_query, {"username": username})
        existing_user = user_check_result.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_id, super_user = existing_user
        update_query = text("UPDATE Users SET Username = :update_username, Email = :email WHERE Username = :username")
        db.execute(
            update_query,
            {"update_username": user_update.Username ,"email": user_update.Email, "username": username}
        )
        db.commit()

        role = "superuser" if super_user else "admin"
        user_data = {
            "user_id": user_id,
            "username": user_update.Username,
            "email": user_update.Email,
            "role": role
        }
        access_token = create_access_token(user_data)

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as http_exc:
        print("An error occurred:", http_exc)
        raise http_exc
    except Exception as e:
        db.rollback()
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    finally:
        db.close()

@app.patch("/users/{username}/password", response_model=dict)
def update_password(username: str, user_update: UserPasswordRequest):
    try:
        db = SessionLocal()

        user_check_query = text("SELECT Id, Password FROM Users WHERE Username = :username")
        user_check_result = db.execute(user_check_query, {"username": username})
        existing_user = user_check_result.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        stored_password_hash = existing_user[1]
        if not pwd_context.verify(user_update.OldPassword, stored_password_hash):
            raise HTTPException(status_code=400, detail="Old password is incorrect")

        new_hashed_password = pwd_context.hash(user_update.NewPassword)

        update_query = text("UPDATE Users SET Password = :new_password WHERE Username = :username")
        db.execute(
            update_query,
            {"new_password": new_hashed_password, "username": username}
        )
        db.commit()

        return {"message": "Password updated successfully"}
    except HTTPException as http_exc:
        print("An error occurred:", http_exc)
        raise http_exc
    except Exception as e:
        db.rollback()
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    finally:
        db.close()

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

        rows = counts_result.fetchall()
        if not rows:
            today_str = datetime.today().strftime('%Y-%m-%d')
            counts.append(CountsGetResponse(
                ManCount=0, WomanCount=0, KidCount=0, StaffCount=0, EmployeeCount=0, TotalCount=0, DateTime=today_str
            ))
        else:
            for row in rows:
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

        rows = counts_result.fetchall()
        if not rows:
            today_str = datetime.today().strftime('%Y-%m-%d')
            counts.append(CountsGetResponseByDateRange(
                ManCount=0, WomanCount=0, KidCount=0, StaffCount=0, EmployeeCount=0,TotalCustomers=0,TotalWorkers=0, TotalCount=0, DateTime=today_str
            ))
        else:
            for row in rows:
                row_dict = row._asdict()
                row_dict['DateTime'] = datetime.strptime(row_dict['DateTime'], '%Y-%m-%d').strftime('%Y-%m-%d')
                counts.append(CountsGetResponseByDateRange(**row_dict))
        
        return counts
    except Exception as e:
        print("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
