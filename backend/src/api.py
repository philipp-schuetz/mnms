import os
from typing import List, Annotated
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

from pydantic import BaseModel


SECRET_KEY = "3487783de8057b7527d133644e25ec84419179ab5a8287215d04d894bbb1e731" # TODO put into env variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# db = TinyDB('/db/db.json', storage=CachingMiddleware(JSONStorage))
db = TinyDB('/db/db.json')

participants_t = db.table('participants')
classes_t = db.table('classes')
groups_t = db.table('groups')
stations_t = db.table('stations')
users_t = db.table('users')

Participant_Q = Query()
Class_Q = Query()
Group_Q = Query()
Station_Q = Query()
User_Q = Query()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str

def group_exists(group_name: str):
    return groups_t.contains(Group_Q.name == group_name)

def class_exists(class_name: str):
    return classes_t.contains(Class_Q.name == class_name)

def get_user(username: str):
    if username == 'admin':
        return {'username': 'admin', 'password': ADMIN_PASSWORD}
    return users_t.get(User_Q.username == username)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if password != user['password']:
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise credentials_exception from exc
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/create")
async def create_user(current_user: Annotated[User, Depends(get_current_user)], username: str, password: str):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        classes = []
        for class_ in classes_t.all():
            classes.append(class_['name'])

        if username not in classes:
            raise HTTPException(status_code=400, detail="username must match any class or group name")

        users_t.insert({
            'username': username,
            'password': password
        })

        return {"message": f"user {username} created"}

@app.get("/")
async def root():
    return {"message": "Visit /docs for the API documentation or go to https://github.com/philipp-schuetz/mnms for further information."}

@app.get("/classes/info")
async def get_class_info(current_user: Annotated[User, Depends(get_current_user)], class_name: str):
    if not class_exists(class_name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="class not found",
        )
    if current_user['username'] != 'admin' and re.sub(r'-\d$', '', current_user['username']) != class_name: # remove group number to convert username to classname
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required or logged in with wrong group",
        )
    else:
        return classes_t.get(Class_Q.name == class_name)

@app.post("/classes/create")
async def create_class(current_user: Annotated[User, Depends(get_current_user)], name: str, room: str, teacher: str):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        class_id = classes_t.insert({
            'name': name,
            'room': room,
            'teacher': teacher
        })
        return {"ID": class_id}

@app.get("/groups/{group}/participants")
async def get_group_participants(current_user: Annotated[User, Depends(get_current_user)], group: str):
    if not group_exists(group):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="group not found",
        )
    if current_user['username'] != 'admin' and current_user['username'] != group:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required or logged in with wrong group",
        )
    else:
        group_participants = participants_t.search(Participant_Q.group == group)
        output = []
        for participant in group_participants:
            participant_with_id = {"id": participant.doc_id}
            participant_with_id.update(participant)
            output.append(participant_with_id)
        return output

@app.get("/groups/{group}/stations")
async def get_group_stations(current_user: Annotated[User, Depends(get_current_user)], group: str):
    if not group_exists(group):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="group not found",
        )
    if current_user['username'] != 'admin' and current_user['username'] != group:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required or logged in with wrong group",
        )
    else:
        stations_res = groups_t.get(Group_Q.name == group)['stations']
        output = {'stations': []}
        for station in stations_res:
            station_info = stations_t.get(Station_Q.name == station)
            output['stations'].append({
                'name': station_info['name'],
                'subject': station_info['subject'],
                'room': station_info['room']
            })
        return output

@app.get("/groups/{group}/scores")
async def get_group_scores(current_user: Annotated[User, Depends(get_current_user)], group: str):
    if not group_exists(group):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="group not found",
        )
    if current_user['username'] != 'admin' and current_user['username'] != group:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required or logged in with wrong group",
        )
    else:
        result = groups_t.get(Group_Q.name == group)
        return {
            "fairness_score": result["fairness_score"],
            "station_scores": result["station_scores"]
        }

@app.get("/groups/get-all")
async def get_all_groups(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        all_groups = groups_t.all()
        out = []
        for group in all_groups:
            out.append(group['name'])
        return out

@app.put("/groups/{group}/scores")
async def set_group_scores(current_user: Annotated[User, Depends(get_current_user)], group: str, fairness: int, score_list: List[int] = [0,0,0,0,0,0]):
    if not group_exists(group):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="group not found",
        )
    if current_user['username'] != 'admin' and current_user['username'] != group:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required or logged in with wrong group",
        )
    else:
        groups_t.update({'fairness_score': fairness}, Group_Q.name == group)
        groups_t.update({'station_scores': score_list}, Group_Q.name == group)
        return

@app.post("/groups/create")
async def create_group(current_user: Annotated[User, Depends(get_current_user)], name:str, stations:List[str]):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        if len(stations) != 8:
            return {"error": "stations should be a list with lenght 8"}
        group_id = groups_t.insert({
            'name': name,
            'fairness_score': 0,
            'station_scores': [0, 0, 0, 0, 0, 0],
            'stations': stations
        })
        return {"ID": group_id}

@app.get("/participants/get-all")
async def get_all_participants(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        return participants_t.all()

@app.post("/participants/create")
async def create_participant(current_user: Annotated[User, Depends(get_current_user)],
                             firstname: str, lastname: str,
                            class_name: str, group_name: str,
                            present: bool = False):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        if not class_exists(class_name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="class not found",
            )
        if not group_exists(group_name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="group not found",
            )
        participant_id = participants_t.insert({
            'firstname': firstname,
            'lastname': lastname,
            'class': class_name,
            'group': group_name,
            'present': present
        })
        return {"ID": participant_id}

@app.put("/participants/set-present")
async def set_participant_present(current_user: Annotated[User, Depends(get_current_user)], participant_id: int, present: bool):
    participants_t.update({'present': present}, doc_ids=[participant_id])

@app.get("/stations/get-all")
async def get_all_stations(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        return stations_t.all()

@app.post("/stations/create")
async def create_station(current_user: Annotated[User, Depends(get_current_user)], name: str, subject: str, room: str):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        station_id = stations_t.insert({
            'name': name,
            'subject': subject,
            'room': room
        })
        return {"ID": station_id}

@app.delete("participants/delete-all")
async def delete_all_participants(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        participants_t.truncate()

@app.delete("/delete-all")
async def delete_all_data(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user['username'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin privileges required",
        )
    else:
        participants_t.truncate()
        classes_t.truncate()
        groups_t.truncate()
        stations_t.truncate()
        users_t.truncate()
