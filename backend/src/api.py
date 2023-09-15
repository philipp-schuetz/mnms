from fastapi import FastAPI

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

from typing import List

app = FastAPI()

# db = TinyDB('db.json', storage=CachingMiddleware(JSONStorage))
db = TinyDB('db.json')

participants_t = db.table('participants')
classes_t = db.table('classes')
groups_t = db.table('groups')
stations_t = db.table('stations')

Participant_Q = Query()
Class_Q = Query()
Group_Q = Query()
Station_Q = Query()

@app.get("/")
async def root():
    return

@app.get("/classes/info")
async def get_class_info(class_name: str):
    return classes_t.get(Class_Q.name == class_name)

@app.post("/classes/create")
async def create_class(name: str, room: str, teacher: str):
    class_id = classes_t.insert({
        'name': name,
        'room': room,
        'teacher': teacher
    })
    print(classes_t.all())
    return {"ID": class_id}

@app.get("/groups/{group}/participants")
async def get_group_participants(group: str):
    return participants_t.search(Participant_Q.group == group)

@app.get("/groups/{group}/stations")
async def get_group_stations(group: str):
    # get station plan for group
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
async def get_group_scores(group: str):
    result = groups_t.get(Group_Q.name == group)
    return {
        "fairness_score": result["fairness_score"],
        "station_scores": result["station_scores"]
    }

@app.put("/groups/{group}/scores")
async def set_group_scores(group: str, fairness: int, score_list: List[int] = [0,0,0,0,0,0]):
    groups_t.update({'fairness_score': fairness}, Group_Q.name == group)
    groups_t.update({'station_scores': score_list}, Group_Q.name == group)
    return

@app.post("/groups/create")
async def create_group(name:str, stations:List[str]):
    if len(stations) != 8:
        return {"error": "stations should be a list with lenght 8"}
    group_id = groups_t.insert({
        'name': name,
        'fairness_score': 0,
        'station_scores': [0, 0, 0, 0, 0, 0],
        'stations': stations
    })
    print(groups_t.all())
    return {"ID": group_id}

@app.post("/participants/create")
async def create_participant(firstname: str, lastname: str,
                    class_name: str, group_name: str,
                    present: bool = False):
    participant_id = participants_t.insert({
        'firstname': firstname,
        'lastname': lastname,
        'class': class_name,
        'group': group_name,
        'present': present
    })
    print(participants_t.all())
    return {"ID": participant_id}

@app.get("/stations/get-all")
async def get_all_stations():
    return stations_t.all()

@app.post("/stations/create")
async def create_station(name: str, subject: str, room: str):
    station_id = stations_t.insert({
        'name': name,
        'subject': subject,
        'room': room
    })
    print(stations_t.all())
    return {"ID": station_id}

@app.delete("participants/delete-all")
async def delete_all_participants(code: int):
    if code == 3594:
        participants_t.truncate()

@app.delete("/delete-all")
async def delete_all_data(code: int):
    if code == 3594:
        participants_t.truncate()
        classes_t.truncate()
        groups_t.truncate()
        stations_t.truncate()
