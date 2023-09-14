import json
from pathlib import Path
import random
import string

class Database():
    def __init__(self, filename:str) -> None:
        self.db_path = Path(filename)

        self.db_content = {}

    def load(self):
        with open(self.db_path, 'r', encoding='UTF-8') as file:
            self.db_content = json.load(file)

    def write(self):
        with open(self.db_path, 'w', encoding='UTF-8') as file:
            json.dump(self.db_content, file)

    def create_id(self):
        characters = string.ascii_lowercase + string.digits
        length = 16
        combination = ''.join(random.choice(characters) for _ in range(length))
        return combination

    def create_participant(self, firstname: str, lastname:str, class_name: str, group: int):
        self.load()
        participant_id = self.create_id()
        self.db_content["participants"][participant_id] = {
            "firstname": firstname,
            "lastname": lastname,
            "class": class_name,
            "group": group,
            "present": False
        }
        self.write()

    def create_class(self, name: str, room:str, teacher: str, total_score: int):
        self.load()
        self.db_content["classes"][name] = {
        "room": room,
        "teacher": teacher,
        "total_score": total_score
        }
        self.write()

    def create_group(self, classname: str, number: int, station_plan: list):
        """group number can be either 1 or 2"""
        self.load()
        name = f'{classname}-{number}'
        self.db_content["groups"][name] = {
            "total_score": 0,
            "fairness_score": 0,
            "station_scores": [0, 0, 0, 0, 0, 0],
            "station_plan": station_plan
        }
        self.write()

    def create_station(self, subject: str, number: int, name: str, room: str):
        """group number can be either 1 or 2"""
        self.load()
        name = f'{subject.lower()}-{number}'
        self.db_content["stations"][name] = {
            "subject": subject,
            "name": name,
            "room": room
        },
        self.write()

    def get_participants(self, classname: str|bool = False, groupname: str|bool = False):
        self.load()
        output = {}
        for participant in self.db_content["participants"]:
            if classname != False:
                if self.db_content["participants"][participant]["class"] == classname:
                    output[participant] = self.db_content["participants"][participant]
            elif groupname != False:
                if self.db_content["participants"][participant]["group"] == groupname:
                    output[participant] = self.db_content["participants"][participant]
        return output

    def change_participant(self,
                           participant_id: str, firstname: str|bool = False,
                           lastname: str|bool = False, classname: str|bool = False,
                           groupname: str|bool = False,present: bool = False
                           ):
        self.load()
        if not not firstname:
            self.db_content["participants"][participant_id]["firstname"] = firstname
        if not not lastname:
            self.db_content["participants"][participant_id]["lastname"] = lastname
        if not not classname:
            self.db_content["participants"][participant_id]["class"] = classname
        if not not groupname:
            self.db_content["participants"][participant_id]["group"] = groupname
        if not not present:
            self.db_content["participants"][participant_id]["present"] = present
        self.write()


    def get_test(self):
        self.load()
        return self.db_content["participants"]

db = Database('db.json')
