from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt" 

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
print('')

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#traversal graph
traversal_graph = {}

#keeps track of prev room
prev_room = None

#keeps track of prev directoin
prev_dir = None

#way to keep track of opposite directions so we can quickly look up opposite direction to update traversal_graph
opposite_directions = {
    'n': 's',
    's': 'n',
    'w': 'e',
    'e': 'w'
}

#keep track of current path in case of dead end
go_back_path = []

#gets direction of an unexplored exit 
def getUnexploredExitDir():
    for direc in traversal_graph[player.current_room.id]:
        if traversal_graph[player.current_room.id][direc] == '?':
            return direc

steps = 0

#go until the traversal graph has the same length as the room graph 
while len(traversal_graph) < len(room_graph):   
    # print(f'Step: {steps}')
    # print('prev dir', prev_dir)
    # print('current room', player.current_room.id)
    # print('traversal path', traversal_path) 
    # print('go back path', go_back_path)
    # print('prev room', prev_room)
    
    
    #get current room exits
    exits = player.current_room.get_exits()
    
    #put room into the traversal graph with the exits that it has 
    if player.current_room.id not in traversal_graph:
        traversal_graph[player.current_room.id] = {}
        #goes through each direction in the exit list
        for direc in exits:
            #puts ? in each direction to mark as unexplored 
            traversal_graph[player.current_room.id][direc] = '?'
    
    #check if coming from previous room 
    if prev_room is not None:
        #updates the current and prev room with the corresponding directions
        traversal_graph[prev_room][prev_dir] = player.current_room.id
        traversal_graph[player.current_room.id][opposite_directions[prev_dir]] = prev_room
        
    #checks if we have visited all rooms before moving again
    if len(traversal_graph) == len(room_graph):
        break
    
    # print('graph', traversal_graph)
    
    #get the first unexplored room using 
    direc = getUnexploredExitDir()

    if direc:
        traversal_path.append(direc)
        go_back_path.append(opposite_directions[direc])
        prev_room = player.current_room.id
        prev_dir = direc
        player.travel(direc)
        traversal_graph[prev_room][direc] = player.current_room.id
        
        steps += 1
    else:
        #if didn't find any ? in current room exits go back the way we came until we find ? 
        while direc is None:
            if len(go_back_path) == 0:
                break
            #get last direction in path
            old_dir = go_back_path.pop()
            traversal_path.append(old_dir)
            player.travel(old_dir)
            direc = getUnexploredExitDir()
            steps += 1
        if len(go_back_path) == 0:
            #resets previous trackers 
            go_back_path = []
        prev_room = None
        prev_dir = None
        
    if steps > 2000:
        break
    # print("---------------------------")
# print('path', traversal_path)
# print("")
# print('graph', traversal_graph)
# print("")


# ---------------------- TRAVERSAL TEST ----------------------
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


