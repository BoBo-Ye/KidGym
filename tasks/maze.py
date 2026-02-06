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
    
    def generate_actions(self) -> list:
        """
        ## Action
            1. choose item number {obj_id}
        """
        
        action_templates = self.get_template()["action"]
        
        actions = []
        for obj in self.grid.objs:
            if obj.c_pk:
                action_template = action_templates["obtain_item"]
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
            1. The agent obtains the diamond. (reward: 1)
            2. Max steps reached. (reward: 0)
        """
        reward, terminated = True, True
        for obj in self.grid.objs:
            if obj.name == "diamond":
                reward, terminated = 0, False
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

    def check_grid(self) -> bool:
        return True