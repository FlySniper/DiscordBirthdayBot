import json
import os.path

FILE = "birthday_db.json"

def read_birthday_file():
    if not os.path.exists(FILE):
        with open(FILE, "w") as birthday_file:
            birthday_file.write(json.dumps({}))
    with open(FILE, "r") as birthday_file:
        data = json.load(birthday_file)
    return data

def write_birthday_file(data):
    with open(FILE, "w") as birthday_file:
        json.dump(data, birthday_file)

def append_to_birthday_file(new_data, name):
    data = read_birthday_file()
    data[name] = new_data
    write_birthday_file(data)

def remove_from_birthday_file(name):
    data = read_birthday_file()
    del data[name]
    write_birthday_file(data)