import requests
import json
import sys


######## SETUP ########

API_URL = 'http://localhost:8000'
CREDENTIALS = {
    "username": "admin",
    "password": "1234"
}

#######################

data = {
    "grant_type": "",
    "username": CREDENTIALS['username'],
    "password": CREDENTIALS['password'],
    "scope": "",
    "client_id": "",
    "client_secret": ""
}

headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}
response = requests.post(f'{API_URL}/token', data=data, timeout=4, headers=headers)

if response.status_code == 200:
    HEADERS = {
        "Authorization": f"Bearer {response.json()['access_token']}",
        "Content-Type": "application/json",
    }
else:
    print('Error: Could not authenticate')
    print(response.status_code)
    sys.exit(1)

def delete_all():
    # delete all documents from the database
    requests.delete(f'{API_URL}/delete-all', headers=HEADERS, timeout=4)

def create_stations():
    url_base = '{api}/stations/create?name={name}&subject={subject}&room={room}'
    stations = [
        {"name": "physik-1", "subject": "Physik I - Raketenbau", "room": "Schulhof"},
        {"name": "physik-2", "subject": "Physik II - Rund um das Fliegen", "room": "PH-H2"},
        {"name": "mathematik-1", "subject": "Mathematik I - Mathematische Knobeleien I", "room": "Obere Brücke"},
        {"name": "mathematik-2", "subject": "Mathematik II - Mathematische Knobeleien II", "room": "222"},
        {"name": "informatik-1", "subject": "Informatik I - Geheime Botschaften", "room": "IN-3"},
        {"name": "geografie-1", "subject": "Geografie I - Atlasralley", "room": "102"},
        {"name": "chemie-1", "subject": "Chemie I - Schaumschläger", "room": "CH-Ü1"},
        {"name": "chemie-2", "subject": "Chemie II - Wer macht den leichtesten Teig?", "room": "CH-Ü2"},
        {"name": "biologie-1", "subject": "Biologie I - 1, 2 oder 3?", "room": "BI-Ü2"},
        {"name": "biologie-2", "subject": "Biologie II - Rätselblitz im Tierreich", "room": "BI-Ü1"},
        {"name": "allgemein-1", "subject": "Allgemein I - Abendessen", "room": "Mensa"},
        {"name": "allgemein-2", "subject": "Allgemein II - Schauexperiment", "room": "Schulhof"}
    ]

    for station in stations:
        requests.post(url_base.format(
            api=API_URL,
            name=station['name'],
            subject=station['subject'],
            room=station['room']
            ),
            headers=HEADERS,
            timeout=4
        )

def create_class(name: str, room: str, teacher: str):
    """class name format: 7midi"""
    requests.post(f'{API_URL}/classes/create?name={name}&room={room}&teacher={teacher}', headers=HEADERS, timeout=4)

def create_group(name: str, stations: list):
    """group name format: 7midi-1; data should be a list containing 8 station names"""
    requests.post(f'{API_URL}/groups/create?name={name}', data=json.dumps(stations), headers=HEADERS, timeout=4)

def create_participant(firstname: str, lastname: str, class_name: str, group_name: str):
    """class name format: 7midi; group name format: 7midi-1"""
    requests.post(
        f'{API_URL}/participants/create?firstname={firstname}&lastname={lastname}&class_name={class_name}&group_name={group_name}&present=false',
        headers=HEADERS,
        timeout=4
        )

def create_user(username: str, password: list):
    """group name format: 7midi-1; data should be a list containing 8 station names"""
    requests.post(f'{API_URL}/users/create?username={username}&password={password}', headers=HEADERS, timeout=4)



delete_all()
create_stations()
create_class('7midi', '123', 'Hr. Bob')
create_group('7midi-1', [
        'mathematik-1',
        'physik-2',
        'chemie-2',
        'allgemein-1',
        'allgemein-2',
        'biologie-1',
        'informatik-1',
        'physik-1',
    ])
create_group('7midi-2', [
        'chemie-2',
        'mathematik-1',
        'physik-2',
        'allgemein-2',
        'allgemein-1',
        'informatik-1',
        'physik-1',
        'biologie-1',
    ])
create_user('7midi-1', '3277')
create_user('7midi-2', '8436')
create_participant('John', 'Doe', '7midi', '7midi-1')
create_participant('Jane', 'Dane', '7midi', '7midi-2')
create_participant('Mike', 'Even', '7midi', '7midi-1')
create_participant('Carol', 'Burnett', '7midi', '7midi-2')


create_class('7wxyz', '123', 'Fr. Alice')
create_group('7wxyz-1', [
        'biologie-1',
        'informatik-1',
        'physik-1',
        'allgemein-1',
        'allgemein-2',
        'mathematik-1',
        'physik-2',
        'chemie-2',
    ])
create_group('7wxyz-2', [
        'informatik-1',
        'physik-1',
        'biologie-1',
        'allgemein-2',
        'allgemein-1',
        'chemie-2',
        'mathematik-1',
        'physik-2',
    ])
create_user('7wxyz-1', '2794')
create_user('7wxyz-2', '4358')
create_participant('Dave', 'Charles', '7wxyz', '7wxyz-1')
create_participant('Frank', 'Miller', '7wxyz', '7wxyz-1')
create_participant('Judy', 'Garland', '7wxyz', '7wxyz-2')
create_participant('Wendy', 'Thomas', '7wxyz', '7wxyz-2')
