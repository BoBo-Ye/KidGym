import json
from src.obj import Obj
from src.task import KidGymTask
from src.config import *
from src.utils import *


class Memory_Maze(KidGymTask):
    """
    ## Description
        This task follows the same rules as the "Maze", with an 
        added challenge. Before the game begins, the agent is shown
        the location of the diamond, but once the game starts, the 
        diamond is hidden among several treasure chests.
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
        treasure = "treasure"
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
        for i in range(2):
            self.grid.add_obj(Obj(treasure, "maze", c_pk=True, visible=False, position_id = 6))
        # wall_num = random.randint(5, 10)
        wall_num = 0
        for i in range(5):
            for j in range(5):
                if self.data[f"{self.iter}"][i][j] == 0:
                    wall_num += 1
        for _ in range(wall_num):
            self.grid.add_obj(Obj(wall, "maze", position_id = 0))
            
        self.goal = self.get_template()["goal"]
        
        return self.goal

    def generate_actions(self) -> list:
        """
        1. pick up object with label {obj_id_1/obj_id_2...}
        2. open the treasure box number {obj.id_3/obj_id_4}
        2. use the item in bag {A/B/C/D} to open {obj_id_5/obj_id_6}
        """
        
        action_templates = self.get_template()["action"]
        
        actions = []  
        if self.cur_step == 0:
            action = action_templates["continue"]
            actions.append(action)
            return actions 
        self.goal = self.get_template()["goal_1"] 
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
    
    def check_goal(self) -> tuple[bool, bool]:
        """
        ## Finish Condition
            1. Obtain the diamond from the treasure chest. (reward: 1)
            2. Obtain the diamond from the wrong treasure chest. (reward: 0)
            3. Max steps reached. (reward: 0)
        """
        reward, terminated = True, True
        num_d = 0
        num_b = 0
        for obj in self.grid.objs:
            if hasattr(obj, "save"):
                num_b += 1
            elif obj.name == "treasure":
                num_d += 1
        if num_d + num_b == 3:    
            reward, terminated = False, False
        elif num_d == 1:
            reward, terminated = False, True

        return reward, terminated 
 
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

    def render(self):
        """
        Render the current scene based on the task.
        """
        if self.cur_step != 0:        
            for obj in self.grid.objs:
                if hasattr(obj, "visible"):
                    obj.visible = True
                if hasattr(obj, "save"):
                    obj.name = "treasure"
                    obj.type = "maze"
        return super().render()

    def check_grid(self) -> bool:
        return True
