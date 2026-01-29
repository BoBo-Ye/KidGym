import random
from src.obj import Obj
from src.task import GridAgentTask
from src.config import *
from src.utils import *

class SimplePick(GridAgentTask):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def generate_scene(self):
        """
        Generate the game based on the task.
        """
        # choose type and add obj
        self.type = TYPES[0]
        names = RandomChoose(RESOURCE[self.type]["resources"], 2)
        for name in names:
            obj = Obj(name, self.type, c_pk=True)
            self.grid.add_obj(obj)
            
    def render(self):
        """
        Render the current scene based on the task.
        """
        return super().render()
        
    def generate_goal(self) -> str:
        """
        Generate goal based on the task(self.goal).
        """
        random_obj = random.choice(self.grid.objs)
        self.target = random_obj.name
        return f"Pick up the {self.target}." 
        
    def generate_actions(self) -> list:
        """
        Generate high-level action list based on the task.
        """
        actions = []
        for obj in self.grid.objs:
            actions.append(f"pick up {obj.name} with label {obj.id}")
        random.shuffle(actions)
        return actions
    
    def extract_actions(self, instruction: str) -> list:
        """
        Extract the low-level actions from the high-level instruction.
        """
        target_obj_id = DecodeFirstNumber(instruction)
        target_obj = self.grid.get_obj_with_id(target_obj_id)
        actions = self.grid.extract_path(target_obj.pos)
        actions.append(ACTION.PICK)
        return actions

    def check_goal(self) -> tuple[bool, bool]:
        """
        Check whether the goal is achieved based on the task.
        Return: task_success(bool), terminated(bool)
        """
        for obj in self.bag.objs:
            if obj and obj.name == self.target:
                return True, True
        return False, False
