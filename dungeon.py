from random import choice, randint


class Dungeon:
    # Variables for managing map state
    map = [[]]
    floor_tiles = []
    wall_tiles = []
    keys = []

    # Character representations
    char_map = {
        'BLANK': ' ',
        'FLOOR': '.',
        'vWALL': '|',
        'hWALL': '-',
        'UNLOCKED_DOOR': '+',
        'LOCKED_DOOR': '#',
        'ENTRANCE': 'E',
        'EXIT': 'X',
        'TREASURE': 'T',
        'KEY': 'K',
    }

    def __init__(self, height, width, max_room_count, min_room_size, max_room_size):
        self.height = height
        self.width = width
        self.max_room_count = max_room_count
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.clear_map()

    def clear_map(self):
        self.map = [x[:] for x in [[self.char_map['BLANK']]*self.width]*self.height]
        self.floor_tiles = []
        self.wall_tiles = []
        self.keys = {}  # dictionary of keys placed mapping to the coordinates they open

    def __str__(self):
        map_content = ""
        for row in self.map:
            row_content = "".join(row)
            map_content = "\n".join([map_content, row_content])
        return map_content

    def get_cell(self, y, x):
        try:
            return self.map[y][x]
        except IndexError:
            return False

    def in_y_bounds(self, y):
        return 0 <= y < self.height

    def in_x_bounds(self, x):
        return 0 <= x < self.width

    def is_corner(self, y, x):
        barriers = [self.char_map['hWALL'], self.char_map['vWALL'], self.char_map['LOCKED_DOOR'], self.char_map['UNLOCKED_DOOR']]
        if ((self.get_cell(y+1, x) in barriers) and (self.get_cell(y, x+1) in barriers) or
            (self.get_cell(y, x+1) in barriers) and (self.get_cell(y-1, x) in barriers) or
            (self.get_cell(y-1, x) in barriers) and (self.get_cell(y, x-1) in barriers) or
            (self.get_cell(y, x-1) in barriers) and (self.get_cell(y+1, x) in barriers)):
            return True
        return False

    def room_in_bounds(self, y1, x1, y2, x2):
        if not self.in_y_bounds(y1) or not self.in_y_bounds(y2) or not self.in_x_bounds(x1) or not self.in_x_bounds(x2):
            return False
        return True

    def area_free(self, y1, x1, y2, x2):
        allowed_tiles = [self.char_map['BLANK'], self.char_map['hWALL'], self.char_map['vWALL']]  # rooms can share walls
        if not self.room_in_bounds(y1, x1, y2, x2):
            return False

        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                if self.get_cell(y, x) not in allowed_tiles:
                    return False
        return True

    # Given a coordinate give a direction pointing away from an adjacent floor tile, if one exists
    def direction_opposing_room(self, y, x):
        direction = None
        if self.get_cell(y+1, x) == self.char_map['FLOOR']:
            direction = 'Down'
        elif self.get_cell(y, x+1) == self.char_map['FLOOR']:
            direction = 'Left'
        elif self.get_cell(y-1, x) == self.char_map['FLOOR']:
            direction = 'Up'
        elif self.get_cell(y, x-1) == self.char_map['FLOOR']:
            direction = 'Right'
        return direction

    # Given the coordinate of a new door to be added, decide if it should be locked and set the tile to a door
    def place_door(self, door_y, door_x):
        if (door_y, door_x) in self.wall_tiles:
            # Decide if this door will be locked
            found_key = False
            for key in self.keys:
                if self.keys[key] is None:
                    weights = [True] + [False]*2
                    choice(weights)
                    self.keys[key] = (door_y, door_x)
                    found_key = True
                    break
            self.map[door_y][door_x] = self.char_map['LOCKED_DOOR'] if found_key else self.char_map['UNLOCKED_DOOR']
            self.wall_tiles.remove((door_y, door_x))

    # Given the dimensions of a room, set the appropriate tiles to floors
    def place_floor(self, y_start, x_start, y_end, x_end):
        for y in range(y_start+1, y_end):
            for x in range(x_start+1, x_end):
                self.map[y][x] = self.char_map['FLOOR']
                self.floor_tiles.append((y, x))

    # Given the dimensions of a room, set the appropriate tiles to walls
    def place_walls(self, y_start, x_start, y_end, x_end):
        for x in range(x_start, x_end+1):
            # top wall
            if self.get_cell(y_start, x) == self.char_map['BLANK']:
                self.map[y_start][x] = self.char_map['hWALL']
                self.wall_tiles.append((y_start, x))
            # bottom wall
            if self.get_cell(y_end, x) == self.char_map['BLANK']:
                self.map[y_end][x] = self.char_map['hWALL']
                self.wall_tiles.append((y_end, x))
        for y in range(y_start, y_end):
            # left wall
            if self.get_cell(y, x_start) == self.char_map['BLANK']:
                self.map[y][x_start] = self.char_map['vWALL']
                self.wall_tiles.append((y, x_start))
            # right wall
            if self.get_cell(y, x_end) == self.char_map['BLANK']:
                self.map[y][x_end] = self.char_map['vWALL']
                self.wall_tiles.append((y, x_end))

    # Given the dimensions of a room, generate random amount of treasure
    def place_treasure(self, y1, x1, y2, x2):
        weights = [0]*3 + [1]*2 + [2]
        amount = choice(weights)
        for i in range(amount):
            treasure_y = randint(y1, y2)
            treasure_x = randint(x1, x2)
            self.map[treasure_y][treasure_x] = self.char_map['TREASURE']
            if (treasure_y, treasure_x) in self.floor_tiles:
                self.floor_tiles.remove((treasure_y, treasure_x))

    # Given the dimensions of a room, randomly generate a key in this room or not
    def place_key(self, y1, x1, y2, x2):
        # Decide whether to place a key in this room or not
        weights = [True] + [False]*7
        place_key = choice(weights)
        if place_key:
            key_y = randint(y1, y2)
            key_x = randint(x1, x2)
            self.keys[(key_y, key_x)] = None
            self.map[key_y][key_x] = self.char_map['KEY']
            if (key_y, key_x) in self.floor_tiles:
                self.floor_tiles.remove((key_y, key_x))

    # Removes any keys that don't map to a door
    def clean_keychain(self):
        for key in self.keys:
            if self.keys[key] is None:
                self.map[key[0]][key[1]] = self.char_map['FLOOR']
                self.floor_tiles.append(self.keys[key])
                del self.keys[key]

    # Given the coordinate for where a door should be placed, generate the dimensions for a room that would start there
    def get_random_dimensions(self, door_y, door_x):
        # initialize coordinates
        y_start = door_y
        x_start = door_x
        y_end = door_y
        x_end = door_x

        # randomize dimensions
        y_length = randint(self.min_room_size, self.max_room_size)
        x_length = randint(self.min_room_size, self.max_room_size)

        # randomly pick where the door will go with respective to the wall, don't pick the ends to stay out of corners
        y_entrance = randint(1, y_length-1)
        x_entrance = randint(1, x_length-1)

        # try to get the direction facing away from a room, if one doesn't exist pick a random direction
        direction = self.direction_opposing_room(door_y, door_x)
        direction = choice(['Up', 'Right', 'Down', 'Left']) if direction is None else direction

        # randomly pick if this will be an expanded room or a hallway
        weights = [True] + [False]*2
        hallway = choice(weights)

        # adjust coordinates, for hallways set width to 3 to include walls and put the door in the middle
        if direction == 'Up':
            y_end += y_length
            x_start -= x_entrance if not hallway else 1
            x_end += x_length-x_entrance if not hallway else 1
        elif direction == 'Right':
            x_end += x_length
            y_start -= y_entrance if not hallway else 1
            y_end += y_length-y_entrance if not hallway else 1
        elif direction == 'Down':
            y_start -= y_length
            x_start -= x_entrance if not hallway else 1
            x_end += x_length-x_entrance if not hallway else 1
        elif direction == 'Left':
            x_start -= x_length
            y_start -= y_entrance if not hallway else 1
            y_end += y_length-y_entrance if not hallway else 1

        return hallway, y_start, x_start, y_end, x_end

    # Attempts to generate a random room and add it to the map.  Returns success bool
    def generate_random_room(self, door_y, door_x):
        hallway, y_start, x_start, y_end, x_end = self.get_random_dimensions(door_y, door_x)

        # if new room fits on the map, set the tiles' symbols
        if self.area_free(y_start, x_start, y_end, x_end):
            self.place_door(door_y, door_x)
            self.place_floor(y_start, x_start, y_end, x_end)
            self.place_walls(y_start, x_start, y_end, x_end)

            if not hallway:
                self.place_treasure(y_start+1, x_start+1, y_end-1, x_end-1)
                self.place_key(y_start+1, x_start+1, y_end-1, x_end-1)

            return True
        else:
            return False

    def generate_random_dungeon(self):
        # clear out any existing map
        self.clear_map()

        # generate first room starting in the middle of the map
        while not self.generate_random_room(self.height//2, self.width//2):
            continue

        # place entrance in first room
        entrance = choice(self.floor_tiles)
        self.map[entrance[0]][entrance[1]] = self.char_map['ENTRANCE']
        self.floor_tiles.remove(entrance)

        # generate the rest of the rooms
        for room in range(self.max_room_count - 1):
            while True:
                next_room = choice(self.wall_tiles)  # choose a random wall to try to attach a new room to
                if not self.is_corner(next_room[0], next_room[1]):  # keep guessing until we find a non-corner wall
                    break
            self.generate_random_room(next_room[0], next_room[1])

        # clean out any keys that didn't get used
        self.clean_keychain()

        # randomly place exit in dungeon
        exit = choice(self.floor_tiles)
        self.map[exit[0]][exit[1]] = self.char_map['EXIT']
        self.floor_tiles.remove(exit)

if __name__ == "__main__":
    # A Quick Example Usage
    d = Dungeon(75, 75, 100, 5, 10)
    d.generate_random_dungeon()
    print(d)
    print("Keys:", d.keys)