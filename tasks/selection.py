from src.obj import Obj
from src.task import KidGymTask
from src.config import *
from src.utils import *

class Selection(KidGymTask):
    """
    ## Description
    Before the game start, some random items will appear in the
    left hint bar. Once the game starts, these items will be 
    hidden from players. The agent need to select the items 
    appeared in the hint bar before.
    """
    def __init__(self, 
                 mem_num: int = 1,
                 **kwargs):
        """
        mem_num: The number of items that will appear on the left side of the game scene. (default: 1)

        Level 1: mem_num = 1
        Level 2: mem_num = 2
        Level 3: mem_num = 3
        """
        super().__init__(**kwargs)
        self.mem_num = mem_num
        self.side_bar = True
        
    def generate_scene_and_goal(self):
        """
        Generate the game based on the task.
        """
        self.side_bar = True
        self.type = RandomChoose(TYPES)
        obj_names = RandomChoose(RESOURCE[self.type]["resources"], self.mem_num)
        self.mem_objs = obj_names
        self.obj = []
        
        goals = []
        if self.mem_num == 1:
            o = Obj(obj_names, self.type, position_id = 1, memorized = True, visible = False, c_pk=True)
            self.grid.add_obj(o)
            self.obj.append(o)
        else:
            for obj in obj_names:
                o = Obj(obj, self.type, position_id = 1, memorized = True, visible = False, c_pk=True)
                self.grid.add_obj(o)
                self.obj.append(o)
        
        if self.mem_num == 1:
            unrelated_objs = RandomChoose(RESOURCE[self.type]["resources"], 3, exclude=self.mem_objs)
        elif self.mem_num == 2:
            unrelated_objs = RandomChoose(RESOURCE[self.type]["resources"], 4, exclude=self.mem_objs)
        elif self.mem_num == 3:
            unrelated_objs = RandomChoose(RESOURCE[self.type]["resources"], 5, exclude=self.mem_objs)

        for obj in unrelated_objs:
            o = Obj(obj, self.type, position_id = 1, visible = False, c_pk=True)
            self.grid.add_obj(o)
        
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
            1. choose {obj_type} number {obj_id}
        """
        
        action_templates = self.get_template()["action"]
        
        actions = []
        if self.cur_step == 0:
            action = action_templates["continue"]
            actions.append(action)
            return actions
        for obj in self.grid.objs:
            action_template = action_templates["choose_item"]
            action = FillTemplate(action_template, {"type": self.type, "obj_id": obj.id})
            actions.append(action)

        random.shuffle(actions)
        return actions

    def get_info_img(self):
        info_bg = np.ones((TILE_PIXEL * 9, TILE_PIXEL * 2, 4), dtype = np.uint8) * 255
        if self.cur_step == 0:
            if self.mem_num == 1:
                mem_img = self.obj[0].img                
            else:
                mem_img = self.obj[0].img
                for obj in self.obj[1:]:
                    mem_img = ImgCombine(mem_img, obj.img, pad_h=True)
            
            info_img = ImgOverlay(info_bg, ImgZoom(mem_img, 0.6), middle_center=True)
            
            return info_img
        
        self.side_bar = False
        self.goal = self.get_template()["goal_1"]
        for obj in self.grid.objs:
            obj.visible = True
        
        return super().get_info_img()
    
    def extract_actions(self, instruction: str) -> list:
        """
        Extract the low-level actions from the high-level instruction.
        """
        if "continue" in instruction:
            return ["continue"]
        
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
        if self.bag.num != self.mem_num:
            return False, False
        
        for i in range(self.bag.num):
            obj = self.bag.objs[i]
            if not hasattr(obj, "memorized"):
                return False, True
        
        return True, True
