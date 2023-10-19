import requests
import json

api_url = 'http://your-api-ip:8000'

def delete_all():
	# delete all documents from the database
	requests.delete(f'{api_url}/delete-all?code=3594')

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
			api=api_url,
			name=station['name'],
			subject=station['subject'],
			room=station['room']
			)
		)

def create_class(name: str, room: str, teacher: str):
	"""class name format: 7midi"""
	requests.post(f'{api_url}/classes/create?name={name}&room={room}&teacher={teacher}')

def create_group(name: str, stations: list):
	"""group name format: 7midi-1; data should be a list containing 8 station names"""
	requests.post(f'{api_url}/groups/create?name={name}', data=json.dumps(stations))

def create_participant(firstname: str, lastname: str, class_name: str, group_name: str):
	"""class name format: 7midi; group name format: 7midi-1"""
	requests.post(f'{api_url}/participants/create?firstname={firstname}&lastname={lastname}&class_name={class_name}&group_name={group_name}&present=false')


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
create_participant('Dave', 'Charles', '7wxyz', '7wxyz-1')
create_participant('Frank', 'Miller', '7wxyz', '7wxyz-1')
create_participant('Judy', 'Garland', '7wxyz', '7wxyz-2')
create_participant('Wendy', 'Thomas', '7wxyz', '7wxyz-2')

