import json
from src.obj import Obj
from src.task import KidGymTask
from src.config import *
from src.utils import *

class Sorting(KidGymTask):
    """
    ## Description
    The agent is presented with a rule that may contradict real-world knowledge.
    For instance, the agent might be instructed that the faster the animal, the 
    heavier it is. The agent is then expected to correctly rank the animals based
    on this given rule.
    
    """
    def __init__(self, 
                 related_num = 2,
                 **kwargs):

        super().__init__(**kwargs)
        self.related_num = related_num    
        self.grid.show_id = False
        self.side_bar = False
        
    def generate_scene_and_goal(self):
        """
        Generate the game based on the task.
        """
        self.correct = 0
        self.type = 'animal'

        goal_templates = self.get_template()["goal"]

        info = json.load(open(f"{JSON_PATH}/{self.name}_L{self.level}.json", "r"))
        if self.related_num == 2:
            self.info = RandomChoose(info)
            self.rule = self.info["rule"]
            IDs = RESOURCE["roman"]["resources"][:2]
            for i in range(2):
                obj = Obj(IDs[i], "roman", relate = self.info["correct"][i])
                self.grid.add_obj(obj)
        elif self.related_num == 3:
            self.info = RandomChoose(info)
            self.rule = self.info["rule"]
            IDs = RESOURCE["roman"]["resources"][:3]
            for i in range(3):
                obj = Obj(IDs[i], "roman", relate = self.info["correct"][i])
                self.grid.add_obj(obj)
        elif self.related_num == 4:
            self.info = RandomChoose(info)
            self.rule = self.info["rule"]
            IDs = RESOURCE["roman"]["resources"][:4]
            for i in range(4):
                obj = Obj(IDs[i], "roman", relate = self.info["correct"][i])
                self.grid.add_obj(obj)

        for i in range(len(self.info["correct"])):
            obj = Obj(self.info["correct"][i], self.type)
            self.bag.add(obj)
        
        self.goal = FillTemplate(goal_templates, {"rule": self.rule, "type": self.type, "property": self.info["property"]})
        
        return self.goal
        
    def generate_actions(self) -> list:
        """
        ## Actions
            1. place {obj} from backpack {bag_id} at grid {pos}
        """
        
        action_templates = self.get_template()["action"]
        
        actions = []
        selections = "ABCD"
        for i in range(self.bag.num):
            for obj in self.grid.objs:
                if hasattr(obj, "relate"):
                    action_template = action_templates["place_item"]
                    action = FillTemplate(action_template, {"type": self.type, "backpack_id": selections[i], "obj_name": obj.name})
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
        bag_id = DecodeFirstLetter(instruction)
        actions.append(ACTION(ACTION.DROP_A + LETTER_TO_NUMBER[bag_id]))
        
        bag_obj = self.bag.get(LETTER_TO_NUMBER[bag_id])
        if bag_obj.name == target_obj.relate:
            self.correct += 1

        return actions

    def check_goal(self) -> tuple[bool, bool]:
        """
        Check whether the goal is achieved based on the task.
        Return: task_success(bool), terminated(bool)
        """
        if self.correct == self.related_num:
            return True, True
        if self.bag.num == 0:
            return False, True
        return False, False
