from src.obj import Obj
from src.task import KidGymTask
from src.config import *
from src.utils import *
import json

class Maze(KidGymTask):
    """
    ## Description
        Agent must obtain the diamond in a maze with several locked doors.
        The agent needs to collect and use the corresponding colored keys 
        to unlock these doors.
    """
    def __init__(self, 
                 match_pairs: int = 1,
                 **kwargs):
        """
        match_pairs: The least number of doors need to be open. (default: 1)

        Level 1: match_pairs = 1
        Level 2: match_pairs = 2
        Level 3: match_pairs = 3
        """
        super().__init__(**kwargs)
        self.match_pairs = match_pairs
        self.side_bar = False

        with open(f'{JSON_PATH}/{self.name}_L{self.level}.json', 'r') as file:
            self.data = json.load(file)

    def generate_scene_and_goal(self):
        """
        Generate the game based on the task.
        """
        self.grid.gen_rule = self.data[f"{self.iter}"]
        self.type = SEQUENCE_TYPE
        keys = RESOURCE["tool"]["key"]
        doors = RESOURCE["tool"]["door"]
        diamond = "diamond"
        wall = RESOURCE["maze"]["resources"]

        self.grid.add_obj(Obj(keys[0], "key", c_pk=True, position_id = 2))
        self.grid.add_obj(Obj(doors[0], "door", c_op=keys[0], position_id = 3))
        if self.match_pairs > 1:
            self.grid.add_obj(Obj(keys[1], "key", c_pk=True, position_id = 2))
            self.grid.add_obj(Obj(doors[1], "door", c_op=keys[1], position_id = 3))
        if self.match_pairs > 2:
            self.grid.add_obj(Obj(keys[2], "key", c_pk=True, position_id = 2))
            self.grid.add_obj(Obj(doors[2], "door", c_op=keys[2], position_id = 3))
            
        self.grid.add_obj(Obj(diamond, "toy", c_pk=True, save=True, position_id = 4))

        wall_num = 0
        for i in range(5):
            for j in range(5):
                if self.data[f"{self.iter}"][i][j] == 0:
                    wall_num += 1
        for _ in range(wall_num):
            self.grid.add_obj(Obj(wall, "maze", position_id = 0))
            
        self.goal = self.get_template()["goal"]
        
        return self.goal

    def render(self):
        """
        Render the current scene based on the task.
        """
        return super().render()
        
    def generate_actions(self) -> list:
        """
        ## Action
            1. choose item number {obj_id}
        """
        
        action_templates = self.get_template()["action"]
        
        actions = []
        for obj in self.grid.objs:
            if obj.c_pk:
                action_template = action_templates["obtain_object"]
                action = FillTemplate(action_template, {"obj_id": obj.id})
                actions.append(action)
            elif hasattr(obj, "c_op"):
                for i in range(self.bag.num):
                    action_template = action_templates["open_door"]
                    action = FillTemplate(action_template, {"backpack_id": BAG_IDS[i], "obj_id": obj.id})
                    actions.append(action)
        random.shuffle(actions)
        return actions
    
    def try_drop(self, idx: int) -> bool:
        """
        Try to drop the object at specific index.
        Based on the task.
        """
        obj = self.agent.get(idx)
        drop_pos = self.agent.get_next_pos()
        next_obj = self.grid.get_obj_with_pos(*drop_pos)
        if next_obj is None:
            return False
        # check if the agent can drop the object
        if next_obj.c_op != obj.name:
            return False
        self.agent.drop(idx)
        self.grid.objs.remove(next_obj)
        return True
    
    def extract_actions(self, instruction: str) -> list:
        """
        Extract the low-level actions from the high-level instruction.
        """
        if "obtain" in instruction:
            target_obj_id = DecodeFirstNumber(instruction)
            target_obj = self.grid.get_obj_with_id(target_obj_id)
            actions = self.grid.extract_path(target_obj.pos)
            actions.append(ACTION.PICK)
        elif "use" in instruction:
            target_bskt_id = DecodeFirstNumber(instruction)
            target_bskt = self.grid.get_obj_with_id(target_bskt_id)
            bag_id = DecodeFirstLetter(instruction)
            actions = self.grid.extract_path(target_bskt.pos)
            actions.append(ACTION(ACTION.DROP_A + LETTER_TO_NUMBER[bag_id]))
        return actions
    
    def check_grid(self) -> bool:                
        return True

    def check_goal(self) -> tuple[bool, bool]:
        """
        ## Finish Condition
            1. The agent obtains the diamond. (reward: 1)
            2. Max steps reached. (reward: 0)
        """
        reward, terminated = True, True
        for obj in self.grid.objs:
            if obj.name == "diamond":
                reward, terminated = 0, False
        return reward, terminated 

# import os
# from src.obj import Obj
# from src.task import GridAgentTask
# from src.config import *
# from src.utils import *
# import itertools

# class Maze(GridAgentTask):
#     """
#     ## Description
#         Agent must obtain the diamond in a maze with several locked doors.
#         The agent needs to collect and use the corresponding colored keys 
#         to unlock these doors.
#     """
#     def __init__(self, 
#                  match_pairs: int = 1,
#                  **kwargs):
#         """
#         match_pairs: The least number of doors need to be open. (default: 1)

#         Level 1: match_pairs = 1
#         Level 2: match_pairs = 2
#         Level 3: match_pairs = 3
#         """
#         super().__init__(**kwargs)
#         self.match_pairs = match_pairs
#         self.side_bar = False

#     def generate_scene_and_goal(self):
#         """
#         Generate the game based on the task.
#         """
#         self.type = SEQUENCE_TYPE
#         keys = RESOURCE["tool"]["key"]
#         doors = RESOURCE["tool"]["door"]
#         diamond = "diamond"
#         wall = RESOURCE["maze"]["resources"]

#         self.grid.add_obj(Obj(keys[0], "key", c_pk=True))
#         self.grid.add_obj(Obj(doors[0], "door", c_op=keys[0]))
#         if self.match_pairs > 1:
#             self.grid.add_obj(Obj(keys[1], "key", c_pk=True))
#             self.grid.add_obj(Obj(doors[1], "door", c_op=keys[1]))
#         if self.match_pairs > 2:
#             self.grid.add_obj(Obj(keys[2], "key", c_pk=True))
#             self.grid.add_obj(Obj(doors[2], "door", c_op=keys[2]))
            
#         self.grid.add_obj(Obj(diamond, "toy", c_pk=True, save=True))
#         wall_num = random.randint(5, 10)
#         for _ in range(wall_num):
#             self.grid.add_obj(Obj(wall, "maze"))
            
#         self.goal = self.get_template()["goal"]
        
#         return self.goal

#     def render(self):
#         """
#         Render the current scene based on the task.
#         """
#         return super().render()
        
#     def generate_actions(self) -> list:
#         """
#         ## Action
#             1. choose item number {obj_id}
#         """
        
#         action_templates = self.get_template()["action"]
        
#         actions = []
#         for obj in self.grid.objs:
#             if obj.c_pk:
#                 action_template = action_templates["obtain_object"]
#                 action = FillTemplate(action_template, {"obj_id": obj.id})
#                 actions.append(action)
#             elif hasattr(obj, "c_op"):
#                 for i in range(self.bag.num):
#                     action_template = action_templates["open_door"]
#                     action = FillTemplate(action_template, {"backpack_id": BAG_IDS[i], "obj_id": obj.id})
#                     actions.append(action)
#         random.shuffle(actions)
#         return actions
    
#     def try_drop(self, idx: int) -> bool:
#         """
#         Try to drop the object at specific index.
#         Based on the task.
#         """
#         obj = self.agent.get(idx)
#         drop_pos = self.agent.get_next_pos()
#         next_obj = self.grid.get_obj_with_pos(*drop_pos)
#         if next_obj is None:
#             return False
#         # check if the agent can drop the object
#         if next_obj.c_op != obj.name:
#             return False
#         self.agent.drop(idx)
#         self.grid.objs.remove(next_obj)
#         return True
    
#     def extract_actions(self, instruction: str) -> list:
#         """
#         Extract the low-level actions from the high-level instruction.
#         """
#         if "obtain" in instruction:
#             target_obj_id = DecodeFirstNumber(instruction)
#             target_obj = self.grid.get_obj_with_id(target_obj_id)
#             actions = self.grid.extract_path(target_obj.pos)
#             actions.append(ACTION.PICK)
#         elif "use" in instruction:
#             target_bskt_id = DecodeFirstNumber(instruction)
#             target_bskt = self.grid.get_obj_with_id(target_bskt_id)
#             bag_id = DecodeFirstLetter(instruction)
#             actions = self.grid.extract_path(target_bskt.pos)
#             actions.append(ACTION(ACTION.DROP_A + LETTER_TO_NUMBER[bag_id]))
#         return actions
    
#     def check_grid(self) -> bool:

#         def bfs(self, grid, queue, visited, visited_key, visited_door):
#             treasure = 0
#             while queue:
#                 x, y = queue.popleft()
#                 for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#                     nx, ny = x + dx, y + dy
#                     # make sure in grid
#                     if not self.grid.in_grid(nx, ny):
#                         continue
#                     # make sure not visited
#                     if (nx, ny) in visited:
#                         continue
#                     # make sure not block
#                     if grid[nx, ny] == 0:
#                         continue
#                     # record visited key
#                     if grid[nx, ny] == 2:
#                         visited_key.append((nx, ny))
#                     #record visited door
#                     if grid[nx, ny] == 3:
#                         visited_door.append((nx, ny))
#                     # add moveable grid in queue
#                     if grid[nx, ny] == 4:
#                         treasure += 1
#                     if grid[nx, ny] == 1:
#                         queue.append((nx, ny))
#                     # mark as visited
#                     visited.add((nx, ny))
                    
#             return visited_key, visited_door, treasure
        
#         def check(self, grid, queue, visited):
#             while queue:
#                 x, y = queue.popleft()
#                 for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#                     nx, ny = x + dx, y + dy
#                     # make sure in grid
#                     if not self.grid.in_grid(nx, ny):
#                         continue
#                     # make sure not visited
#                     if (nx, ny) in visited:
#                         continue
#                     # make sure not block
#                     if grid[nx, ny] == 0:
#                         continue
#                     if grid[nx, ny] != 0:
#                         queue.append((nx, ny))
#                     # mark as visited
#                     visited.add((nx, ny))         
#             return len(visited)
            
#         grid = np.ones((GRID_SIZE, GRID_SIZE), dtype=int)
        
#         can_walk = 25
#         for obj in self.grid.objs:
#             if not obj.c_pk and not hasattr(obj, "c_op"):
#                 can_walk -= 1
        
#         for obj in self.grid.objs:
#             if obj.pos is None:
#                 return False
#             if obj.c_pk:
#                 if not hasattr(obj, "save"):
#                     grid[obj.pos[1]][obj.pos[0]] = 2
#                 else:
#                     grid[obj.pos[1]][obj.pos[0]] = 4 # treasure
#             elif hasattr(obj, "c_op"):
#                 grid[obj.pos[1]][obj.pos[0]] = 3
#             else:
#                 grid[obj.pos[1]][obj.pos[0]] = 0

#         def check_connection_conditions(grid, rows, cols):
#             visited = [[False for _ in range(cols)] for _ in range(rows)]
            
#             for i in range(rows):
#                 for j in range(cols):
#                     if grid[i][j] == 0 and not visited[i][j]:
#                         queue = deque()
#                         queue.append((i, j))
#                         visited[i][j] = True
#                         has_outer = False
#                         while queue:
#                             x, y = queue.popleft()
#                             if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
#                                 has_outer = True
#                             for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                                 nx = x + dx
#                                 ny = y + dy
#                                 if 0 <= nx < rows and 0 <= ny < cols:
#                                     if grid[nx][ny] == 0 and not visited[nx][ny]:
#                                         visited[nx][ny] = True
#                                         queue.append((nx, ny))
#                         if not has_outer:
#                             return False
#             return True
        
#         if not check_connection_conditions(grid, GRID_SIZE, GRID_SIZE):
#             return False
        
#         # def check_door(grid):
#         #     if self.match_pairs == 1:
#         #         return True
#         #     doors = []
#         #     keys = []
#         #     for i in range(GRID_SIZE):
#         #         for j in range(GRID_SIZE):
#         #             if grid[i][j] == 3:
#         #                 doors.append((i, j))  
#         #     for i in range(GRID_SIZE):
#         #         for j in range(GRID_SIZE):
#         #             if grid[i][j] == 2:
#         #                 keys.append((i, j))  
#         #                 grid[i][j] = 1
#         #     combinations = list(itertools.combinations(doors, self.match_pairs - 1))
#         #     for combination in combinations:
#         #         for item in combination:
#         #             grid[item[0]][item[1]] = 1
#         #         _, _, treasure = bfs(self, grid, deque([tuple(self.agent.pos[::-1])]), set([tuple(self.agent.pos[::-1])]), [], [])
#         #         for item in combination:
#         #             grid[item[0]][item[1]] = 3
#         #         if treasure == 1:
#         #             for item in keys:
#         #                 grid[item[0]][item[1]] = 2
#         #             return False
#         #     for item in keys:
#         #         grid[item[0]][item[1]] = 2
#         #     return True
        
#         # test_grid = grid
#         # if check_door(test_grid) == False:
#         #     return False

#         # invert x,y
#         start_pos = tuple(self.agent.pos[::-1])
#         queue = deque([start_pos])
#         visited = set([start_pos])
#         visited_key = []
#         visited_door = []   
#         if check(self, grid, queue, visited) != can_walk:
#             return False               
        
#         queue = deque([start_pos])
#         visited = set([start_pos])
        
#         round = 0
        
#         self.valid_key_positions = []
#         self.valid_door_positions = []
        
#         while (round < (len(self.grid.objs) - 1) / 2):
#             _, _, treasure = bfs(self, grid, queue, visited, visited_key, visited_door)
#             if round > 0 and treasure == 1:
#                 return True
#             if len(visited_key) == 0:
#                 return False
#             else:
#                 num = 0 # number of doors can be open
#                 key_visited = visited_key
#                 for key in self.grid.objs:
#                     if tuple(key.pos[::-1]) in key_visited:
#                         grid[key.pos[1]][key.pos[0]] = 1
#                         queue = deque([start_pos])
#                         visited = set([start_pos])
#                         visited_key = []
#                         visited_door = []
#                         _, _, treasure = bfs(self, grid, queue, visited, visited_key, visited_door)
#                         if treasure == 1:
#                             return False
#                         for door in self.grid.objs:
#                             if tuple(door.pos[::-1]) in visited_door:
#                                 if hasattr(door, "c_op") and key.name == door.c_op:
#                                     num += 1
#                                     key_record = key
#                                     door_record = door
#                         grid[key.pos[1]][key.pos[0]] = 2
#                 if num != 1:
#                     return False
#                 grid[key_record.pos[1]][key_record.pos[0]] = 1
#                 self.valid_key_positions.append(key_record.pos)
#                 self.valid_door_positions.append(door_record.pos)
#                 grid[door_record.pos[1]][door_record.pos[0]] = 1
#                 queue = deque([start_pos])
#                 visited = set([start_pos])
#                 visited_key = []
#                 visited_door = []
#                 round += 1
        
#         _, _, treasure = bfs(self, grid, queue, visited, visited_key, visited_door)
#         if treasure == 0:
#             return False
                
#         return True

#     def check_goal(self) -> tuple[bool, bool]:
#         """
#         ## Finish Condition
#             1. The agent obtains the diamond. (reward: 1)
#             2. Max steps reached. (reward: 0)
#         """
#         reward, terminated = True, True
#         for obj in self.grid.objs:
#             if obj.name == "diamond":
#                 reward, terminated = 0, False
#         return reward, terminated 
