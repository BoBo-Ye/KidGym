from src.obj import Obj
from src.task import KidGymTask 
from src.config import *
from src.utils import *

class Placement(KidGymTask):
    """
    ## Description
        The agent is required to place the item in the opposite position based on the given goal.
    """
    def __init__(self, 
                 level: int = 1,
                 **kwargs):

        super().__init__(**kwargs)
        self.level = level
        if self.level == 1:
            self.grid.gen_rule = [[0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 5, 1, 'A'],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]] 
        else:
            self.grid.gen_rule = [[0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 5, 1, 'A'],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]]   
        self.grid.show_id = False
        self.side_bar = False

    def generate_scene_and_goal(self):
        """
        Generate the game based on the task.
        """
        self.type = RandomChoose(TYPES)
        if self.level == 1:
            self.roman = RESOURCE["roman"]["resources"][:4]
            self.orientation = RandomChoose(ORIENTATION_4)
        else:
            self.roman = RESOURCE["roman"]["resources"][:8]
            self.orientation = RandomChoose(ORIENTATION_8)
        for i in range(len(self.roman)):
            obj = Obj(self.roman[i], "roman", position_id = 1)
            self.grid.add_obj(obj)
            
        middle_obj = RandomChoose(RESOURCE[self.type]["resources"], 1)
        self.center = Obj(middle_obj, self.type, position_id=5)
        self.grid.add_obj(self.center)
        place_obj_type = RandomChoose(TYPES)
        place_obj = RandomChoose(RESOURCE[place_obj_type]["resources"], 1, exclude=middle_obj)
        obj = Obj(place_obj, place_obj_type, c_pk=True) 
        self.place_obj = obj
        self.bag.add(obj)
        
        self.direction = RandomChoose(DIRECTION)
        
        goal_templates = self.get_template()["goal"]
        
        if self.level == 1:
            self.goal = FillTemplate(goal_templates, {"place_obj_name": self.place_obj.name, "orientation": self.orientation, "center_name": self.center.name})
        else:
            self.goal = FillTemplate(goal_templates, {"place_obj_name": self.place_obj.name, "clock_direction": self.direction, "orientation": self.orientation, "center_name": self.center.name})
        
        return self.goal
        
    def generate_actions(self) -> list:
        """
        ## Action
            1. choose item number {obj_id}
        """
        
        action_templates = self.get_template()["action"]
        
        actions = []
        for i in range(0, len(self.roman)):
            action_template = action_templates["place_object"]
            action = FillTemplate(action_template, {"place_obj_name": self.place_obj.name, "grid_id": self.roman[i]})
            actions.append(action)
        random.shuffle(actions)
        return actions
    
    def extract_actions(self, instruction: str) -> list:
        """
        Extract the low-level actions from the high-level instruction.
        """
        target_pos_name = DecodeFirstRoman(instruction)
        target_obj = self.grid.get_obj_with_name(target_pos_name)
        actions = self.grid.extract_path(target_obj.pos)
        self.grid.objs.remove(target_obj)
        bag_id = 'A'
        actions.append(ACTION(ACTION.DROP_A + LETTER_TO_NUMBER[bag_id]))

        return actions
    
    def check_grid(self) -> bool:
        return True

    def check_goal(self) -> tuple[bool, bool]:
        """
        ## Finish Condition
            1. The agent has placed the item in the correct position. (reward = 1)
            2. The agent has placed the item in the wrong position. (reward = 0)
        """
        
        direction_mapping_level1 = {
            "north": (0, 1),
            "south": (0, -1),
            "west": (1, 0),
            "east": (-1, 0)}
        
        direction_mapping_level2 = {
            "north": (0, 1),
            "south": (0, -1),
            "west": (1, 0),
            "east": (-1, 0),
            "northwest": (1, 1),
            "southwest": (1, -1),
            "northeast": (-1, 1),
            "southeast": (-1, -1)
        }

        direction_mapping_level3 = {
            "north": {
                "clockwise": (-1, 1),      
                "anticlockwise": (1, 1) },
            "south": {
                "clockwise": (1, -1),         
                "anticlockwise": (-1, -1)},
            "west": {
                "clockwise": (1, 1),     
                "anticlockwise": (1, -1)},
            "east": {
                "clockwise": (-1, -1),         
                "anticlockwise": (-1, 1)},
            "northeast": {
                "clockwise": (-1, 0),      
                "anticlockwise": (0, 1) },
            "southeast": {
                "clockwise": (0, -1),         
                "anticlockwise": (-1, 0)},
            "northwest": {
                "clockwise": (0, 1),     
                "anticlockwise": (1, 0)},
            "southwest": {
                "clockwise": (1, 0),         
                "anticlockwise": (0, -1)}
        }
        
        if self.level == 1:
            target_pos = (2 + direction_mapping_level1[self.orientation][0],
                      2 + direction_mapping_level1[self.orientation][1])
        elif self.level == 2:
            target_pos = (2 + direction_mapping_level2[self.orientation][0],
                      2 + direction_mapping_level2[self.orientation][1])
        else:
            target_pos = (2 + direction_mapping_level3[self.orientation][self.direction][0],
                      2 + direction_mapping_level3[self.orientation][self.direction][1])

        if not self.bag.empty:
            return False, False
        
        obj = self.grid.get_obj_with_pos(*target_pos)
        if obj.c_pk:
            return True, True
        return False, True
