def has_room(store, room_type):
    return store.rooms.get(room_type, 0) > 0


def reserve(store, room_type):
    if not has_room(store, room_type):
        return False
    store.rooms[room_type] -= 1
    return True
