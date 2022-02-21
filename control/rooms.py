from collections import namedtuple

from connect import get_cursor


def get_room_attrs(sql: str, params: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, params)

    room_dict = {
        "bldg": params[0],
        "room_no": params[1],
        "capacity": 0,
        "attributes": []
    }
    for r in cursor:
        room_dict["capacity"] = r[2]
        room_dict["attributes"].append((r[3].strip(), r[4]))

    print(room_dict)
    return(room_dict)


def get_rooms(sql: str, params: tuple) -> tuple:
    cursor = get_cursor()
    cursor.execute(sql, params)
    rooms = []

    for r in cursor:
        rooms.append(r)

    return tuple(rooms)
    


def get_room_availability(sql: str, params: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, params)
    avail_rooms_dict = {
        "rooms": []
    }

    for r in cursor:
        avail_rooms_dict["rooms"].append(r)


    return avail_rooms_dict


def get_rooms_by_capacity(sql: str, params: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, params)
    found_rooms = {'rooms': [r for r in cursor]}
    return found_rooms


def find_new_room_for_sln(sql: str, params: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, params)
    found_rooms = {"rooms": [r for r in cursor]}
    return found_rooms


if __name__ == "__main__":
    room_attrs = get_room_attrs('ECE', '042')
