from fastapi import FastAPI

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

from typing import List

app = FastAPI()

# db = TinyDB('db.json', storage=CachingMiddleware(JSONStorage))
db = TinyDB('db.json')

participants = db.table('participants')
classes = db.table('classes')
groups = db.table('groups')
stations = db.table('stations')

Participant_Q = Query()
Class_Q = Query()
Group_Q = Query()
Station_Q = Query()

@app.get("/")
async def root():
    return

@app.post("/classes/create")
async def create_class(name: str, room: str, teacher: str):
    class_id = classes.insert({
        'name': name,
        'room': room,
        'teacher': teacher
    })
    print(classes.all())
    return {"ID": class_id}

@app.get("/classes/info")
async def get_class_info(class_name: str):
    return classes.get(Class_Q.name == class_name)

@app.post("/groups/create")
async def create_group(name:str, stations:List[str]):
    if len(stations) != 8:
        return {"error": "stations should be a list with lenght 8"}
    group_id = groups.insert({
        'name': name,
        'fairness_score': 0,
        'station_scores': [0, 0, 0, 0, 0, 0],
        'stations': stations
    })
    print(groups.all())
    return {"ID": group_id}

@app.get("/groups/{group}/participants")
async def get_group_participants(group: str):
    return participants.search(Participant_Q.group == group)

@app.get("/groups/{group}/scores")
async def get_group_scores(group: str):
    result = groups.search(Group_Q.name == group)
    return {
        "fairness_score": result["fairness_score"],
        "station_scores": result["station_scores"]
    }

@app.put("/groups/{group}/scores")
async def set_group_scores(group: str, fairness: int,
                           station_one: int, station_two: int,
                           station_three: int, station_four: int,
                           station_five: int, station_six: int):
    groups.update({'fairness_score': fairness}, Group_Q.name == group)
    groups.update({'station_scores': [
                            station_one,
                            station_two,
                            station_three,
                            station_four,
                            station_five,
                            station_six
                    ]}, Group_Q.name == group)

@app.get("/groups/{group}/stations")
async def get_group_stations(group: str):
    stations_res = groups.get(Group_Q.name == group)['stations']
    output = {'stations': {}}
    for station in stations_res:
        station_info = stations.search(Station_Q.name == station)
        output['stations'][station] = {
            'name': station_info['name'],
            'room': station_info['room']
		}
    return output

@app.post("/participants/create")
async def create_participant(firstname: str, lastname: str,
                    class_name: str, group_name: str,
                    present: bool = False):
    participant_id = participants.insert({
        'firstname': firstname,
        'lastname': lastname,
        'class': class_name,
        'group': group_name,
        'present': present
    })
    print(participants.all())
    return {"ID": participant_id}

# TODO create, read for stations

# TODO delete for all the other stuff

@app.delete("participants/delete-all")
async def delete_all_participants(code: int):
    if code == 3594:
        participants.truncate()

@app.delete("/delete-all")
async def delete_all_data(code: int):
    if code == 3594:
        db.truncate()
