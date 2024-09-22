from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.utils import log_ip_country_weather
from . import auth, models, schemas, crud, database
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, oauth2_scheme, verify_token

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tasks", response_model=schemas.TaskResponse)
@log_ip_country_weather
async def create_task(request: Request, task: schemas.TaskCreate, db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    username = auth.verify_token(token, HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ))
    return crud.create_task(db=db, task=task)

@app.get("/tasks", response_model=list[schemas.TaskResponse])
@log_ip_country_weather
async def get_tasks(request: Request, db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token, HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ))
    return crud.get_tasks(db=db)

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
@log_ip_country_weather
async def get_task(request: Request, task_id: int, db: Session = Depends(database.get_db), 
                   token: str = Depends(oauth2_scheme)):
    verify_token(token, HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ))
    task = crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
@log_ip_country_weather
async def update_task(request: Request, task_id: int, task: schemas.TaskUpdate, db: Session = Depends(database.get_db),
                      token: str = Depends(oauth2_scheme)):
    verify_token(token, HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ))
    task_updated = crud.update_task(db=db, task_id=task_id, task=task)
    if task_updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_updated

@app.delete("/tasks/{task_id}")
@log_ip_country_weather
async def delete_task(request: Request, task_id: int, db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token, HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ))
    task_deleted = crud.delete_task(db=db, task_id=task_id)
    if task_deleted is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}


@app.post("/users/", response_model=schemas.UserOut)
@log_ip_country_weather
def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Get all users
@app.get("/users/", response_model=list[schemas.UserOut])
@log_ip_country_weather
def read_users(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Get a user by ID
@app.get("/users/{user_id}", response_model=schemas.UserOut)
@log_ip_country_weather
def read_user(request: Request, user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/api/logs")
def get_api_logs(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    logs = crud.get_api_log(db, skip=skip, limit=limit)
    if logs is None:
        raise HTTPException(status_code=404, detail="User not found")
    return logs