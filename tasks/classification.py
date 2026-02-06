from src.obj import Obj
from src.task import KidGymTask
from src.config import *
from src.utils import *

class Classification(KidGymTask):
    def __init__(self, 
                 type_num: int = 2,
                 item_num: int = 2,
                 **kwargs):
        """
        type_num: How many types of objects to classify.
        item_num: How many items of each type to classify.

        Level 1: type_num = 2, item_num = 1
        Level 2: type_num = 2, item_num = 2
        Level 3: type_num = 2, item_num = 3

        """
        super().__init__(**kwargs)
        self.type_num = type_num
        self.item_num = item_num
        self.side_bar = False
        
    def generate_scene_and_goal(self):
        """
        "goal": "Place {item_1} in the {color_1} basket and {item_2} in the {color_2} basket."
        """

        self.type = RandomChoose(TYPES)
        items = RandomChoose(RESOURCE[self.type]["resources"], self.type_num)
        colors = RandomChoose(RESOURCE["tool"]["basket"], self.type_num)
        
        goal_template = self.get_template()["goal"]
        goal_values = {
            "item_1": items[0],
            "item_2": items[1],
            "color_1": colors[0],
            "color_2": colors[1],
        }
        self.goal = FillTemplate(goal_template, goal_values)
        
        # Add objects to the grid for all type_num values
        for i in range(self.type_num):
            for _ in range(self.item_num):
                obj = Obj(items[i], self.type, c_pk=True)
                self.grid.add_obj(obj)
            bskt = Obj(colors[i], "basket", c_pk=False, c_ct=items[i])
            self.grid.add_obj(bskt)
        
        return self.goal

    def generate_actions(self) -> list:
        """
        "pick_item": "pick up the item with label {item_id}"
        "put_item": "put the item from backpack {bag_id} into the basket with label {basket_id}"
        """
        
        action_templates = self.get_template()["action"]
        actions = []
        for obj in self.grid.objs:
            # "pick_item"
            if obj.get_attr("c_pk"):
                action_template = action_templates["pick_item"]
                action = FillTemplate(action_template, {"item_id": obj.id})
                actions.append(action)
            # "put_item"
            else:
                for i in range(self.bag.size):
                    if self.bag.objs[i] is not None:
                        action_template = action_templates["put_item"]
                        action = FillTemplate(action_template, {"backpack_id": BAG_IDS[i], "basket_id": obj.id})
                        actions.append(action)
                        
        return actions

    def check_goal(self) -> tuple[bool, bool]:
        """
        Check whether the goal is achieved based on the task.
        Return: task_success(bool), terminated(bool)
        """
        # no pickable objs in the scene
        for obj in self.grid.objs:
            if obj.c_pk == True:
                return False, False
        # no remaining objs in the backpack
        for obj in self.bag.objs:
            if obj is not None:
                return False, False
        return True, True
    
    def try_drop(self, idx: int) -> bool:
        """
        Try to drop the object at specific index.
        Based on the task.
        """
        obj = self.agent.get(idx)
        drop_pos = self.agent.get_next_pos()
        next_obj = self.grid.get_obj_with_pos(*drop_pos)
        # check if the agent can drop the object
        if next_obj.c_ct != obj.name:
            return False
        self.agent.drop(idx)
        return True
    