import random
from src.obj import Obj
from src.task import KidGymTask
from src.config import *
from src.utils import *

class Counting(KidGymTask):
    def __init__(self, 
                 type_num: int = 1,
                 range: tuple = (1, 3),
                 **kwargs):
        
        super().__init__(**kwargs)
        
        """
        type_num: The number of piles that will appear for each quantity. (default: 1)
        range: The range of the target number. (default: (1, 3))

        Level 1: type_num = 1, range = (1, 3)
        Level 2: type_num = 2, range = (2, 6)
        Level 3: type_num = 3, range = (3, 9)
        """
        self.type_num = type_num
        self.range = range
        self.side_bar = False  
        self.task_terminate = False
        
    def generate_scene_and_goal(self):
        """
        Generate the game based on the task.
        """
        # choose different objs with the same type
        self.type = RandomChoose(COUNTING_TYPES)
        obj_names = RandomChoose(RESOURCE[self.type]["counting_resourses"], 1)
        self.obj_name = obj_names
        self.collect_num = random.randint(*self.range)
        
        goal_template = self.get_template()["goal"]
        goal_values = {
            "number": self.collect_num,
            "item": obj_names
        }
        self.goal = FillTemplate(goal_template, goal_values)
        
        for _ in range(self.type_num):
            for j in range(3):
                obj = Obj(f"{obj_names}_{j+1}", self.type, c_pk=True, value=j+1)
                self.grid.add_obj(obj)

        return self.goal
            
    def render(self):
        """
        Render the current scene based on the task.
        """
        return super().render()
        
    def generate_actions(self) -> list:
        """
        ## Action
            1. pick up {obj_name} number {obj_id}
        """
        
        action_templates = self.get_template()["action"]
        
        actions = []
        for obj in self.grid.objs:
            action_template = action_templates["pick_item"]
            action = FillTemplate(action_template, {"item": self.obj_name, "item_id": obj.id})
            actions.append(action)
            
        action_template = action_templates["end_task"]
        action = FillTemplate(action_template, {"number": self.collect_num, "item": self.obj_name})
        actions.append(action)   
        return actions
    
    def extract_actions(self, instruction: str) -> list:
        """
        Extract the low-level actions from the high-level instruction.
        """
        self.task_terminate = False
        if "I" in instruction:
            self.task_terminate = True
            return [ACTION.ROTATE]
        target_obj_id = DecodeFirstNumber(instruction)
        target_obj = self.grid.get_obj_with_id(target_obj_id)
        actions = self.grid.extract_path(target_obj.pos)
        actions.append(ACTION.PICK)
        return actions
    
    def check_grid(self) -> bool:
        return super().check_grid()

    def check_goal(self) -> tuple[bool, bool]:
        """
        Check whether the goal is achieved based on the task.
        Return: task_success(bool), terminated(bool)
        """
        value = 0
        for obj in self.bag.objs:
            if obj:
                value += obj.value
        
        if self.task_terminate:
            if value == self.collect_num:
                # print("Game success! You collected {num}/{_num}!".format(num=value, _num=self.collect_num))
                return True, True
            else:
                # print("Game failed! You collected {num}/{_num}!".format(num=value, _num=self.collect_num))
                return False, True
        if self.agent.bag.full and value < self.collect_num:
            # print("Game failed! You collected {num}/{_num}!".format(num=value, _num=self.collect_num))
            return False, True

        return False, False
