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



if __name__ == "__main__":
    room_attrs = get_room_attrs('ECE', '042')
