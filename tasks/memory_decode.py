from src.obj import Obj
from src.task import KidGymTask
from src.config import *
from src.utils import *

class Memory_Decode(KidGymTask):
    """
    ## Description
    This task follows the same rules as "Decode". The agent must
    additionally remember the relationships indicated in the code
    table, which will disappear once the game starts.
    """

    def __init__(self, 
                 related_num: int = 1,
                 **kwargs):
        """
        related_num: The number of item pairs that will appear in the code table. (default: 1)
        
        Level 1: related_num = 1
        Level 2: related_num = 2
        Level 3: related_num = 3
        """
        super().__init__(**kwargs)
        self.related_num = related_num
        self.side_bar = True

    def generate_scene_and_goal(self):
        """
        Generate the game based on the task.
        """
        if self.related_num < 4:
            
            self.type = DECODE_TYPE
            objs_1_type = RandomChoose(TYPES)
            objs_2_type = RandomChoose(TYPES)
            objs_1 = RandomChoose(RESOURCE[objs_1_type]["resources"], self.related_num)
            objs_2 = RandomChoose(RESOURCE[objs_2_type]["resources"], self.related_num, exclude=objs_1)
            self.objs_1 = []
            self.objs_2 = []
            if self.related_num == 1:
                self.objs_1 = Obj(objs_1, objs_1_type)
                self.objs_2 = Obj(objs_2, objs_2_type)
            else:
                for obj in objs_1:
                    self.objs_1.append(Obj(obj, objs_1_type))
                for obj in objs_2:
                    self.objs_2.append(Obj(obj, objs_2_type))
            
            target_id = np.random.randint(0, self.related_num)
            target_obj = objs_1[target_id] if self.related_num > 1 else objs_1
            self.target_obj = Obj(target_obj, objs_1_type, position_id = 1)
            related_obj = objs_2[target_id] if self.related_num > 1 else objs_2
            obj = Obj(related_obj, objs_2_type, position_id = 2, c_pk=True, related_name = target_obj)
            self.grid.add_obj(obj)
            
            exclude=[target_obj, related_obj]
            for i in range(self.related_num * 2 + 1):
                type = RandomChoose(TYPES)
                new_obj = RandomChoose(RESOURCE[type]["resources"], 1, exclude)
                obj = Obj(new_obj, type, position_id = 2, c_pk=True)
                self.grid.add_obj(obj)
                exclude.append(new_obj)
                
            self.goal = self.get_template()["goal"]
            
        else:
            
            self.type = DECODE_TYPE
            obj_type = RandomChoose(TYPES)
            objs_1 = RandomChoose(RESOURCE[obj_type]["resources"], 3)
            objs_2 = objs_1.copy()
            objs_2[0] = objs_1[2]
            objs_2[1] = objs_1[0]
            objs_2[2] = objs_1[1]
            self.objs_1 = []
            self.objs_2 = []
            for obj in objs_1:
                self.objs_1.append(Obj(obj, obj_type))
            for obj in objs_2:
                self.objs_2.append(Obj(obj, obj_type))
            
            target_id = np.random.randint(0, 3)
            target_obj = objs_1[target_id]
            self.target_obj = Obj(target_obj, obj_type, position_id = 1)
            related_obj = objs_2[(target_id + 2) % 3]
            obj = Obj(related_obj, obj_type, position_id = 2, c_pk=True, related_name = target_obj)
            self.grid.add_obj(obj)
            for i in range(3):
                if i != (target_id + 2) % 3:
                    new_obj = objs_2[i]
                    obj = Obj(new_obj, obj_type, position_id = 2, c_pk=True)
                    self.grid.add_obj(obj)
            
            exclude=[target_obj, related_obj]
            for i in range(5):
                type = RandomChoose(TYPES)
                new_obj = RandomChoose(RESOURCE[type]["resources"], 1, exclude)
                obj = Obj(new_obj, type, position_id = 2, c_pk=True)
                self.grid.add_obj(obj)
                exclude.append(new_obj)
                
            self.goal = "In the first image, three arrow-connected items with one-to-one correspondence(s) will be shown on the left margin that you need to remember. In the following images, the correspondence(s) will not be shown, and a target item will be generated in the black box in the upper left corner. Starting from the target, you should map *twice* in sequence and then select the corresponding item in the scene."

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
        if self.cur_step == 0:
            action = action_templates["continue"]
            actions.append(action)
            return actions
        for obj in self.grid.objs:
            if obj.position_id == 2:
                action_template = action_templates["choose_item"]
                action = FillTemplate(action_template, {"item_id": obj.id})
                actions.append(action)
        random.shuffle(actions)
        return actions
    
    def render_decode_relationship(self, obj_1: Obj, obj_2: Obj):
        # copy transparent fg_img to white bg
        white_bg = np.ones((TILE_PIXEL, TILE_PIXEL, 4), dtype = np.uint8) * 255
        obj_1_img = ImgOverlay(white_bg, ImgZoom(obj_1.img, 0.5), middle_center=True)
        obj_2_img = ImgOverlay(white_bg, ImgZoom(obj_2.img, 0.5), middle_center=True)
        # combine two obj imgs and add arrow
        arrow_img = LoadImage(f"{IMG_BASE_PATH}/game/arrow.png")
        relationship_img = ImgOverlay(ImgCombine(obj_1_img, obj_2_img, pad_h=False), ImgZoom(arrow_img, 0.2), middle_center=True)
        return relationship_img
    
    def render_decode_relationships(self, objs_1: list[Obj], objs_2: list[Obj]):
        if self.related_num == 1:
            relationship_img = self.render_decode_relationship(objs_1, objs_2)
            return relationship_img
        
        relationship_imgs = []
        for obj_1, obj_2 in zip(objs_1, objs_2):
            relationship_imgs.append(self.render_decode_relationship(obj_1, obj_2))
        # combine all relationship imgs into a table
        relationship_table_img = relationship_imgs[0]
        for i in range(1, len(relationship_imgs)):
            relationship_table_img = ImgCombine(relationship_table_img, relationship_imgs[i], pad_h = True)
        return relationship_table_img
    
    def get_info_img(self):
        if self.cur_step == 0:
            render_table_fg = self.render_decode_relationships(self.objs_1, self.objs_2)
            info_bg = np.ones((TILE_PIXEL * 9, TILE_PIXEL * 2, 4), dtype = np.uint8) * 255
            info_bg = ImgOverlay(info_bg, render_table_fg, middle_center=True)
            return info_bg
        else:
            # self.side_bar = False
            self.goal = self.get_template()["goal_1"]
            info_bg = np.ones((TILE_PIXEL * 9, TILE_PIXEL * 2, 4), dtype = np.uint8) * 255
            render_table_fg = self.render_decode_relationships(self.objs_1, self.objs_2)        
            target_img = ImgOverlay(ImgZoom(LoadImage(f"{IMG_BASE_PATH}/game/bag_grid.png"), 0.6), ImgZoom(self.target_obj.img, 0.6), middle_center=True)
            info_bg = ImgOverlay(info_bg, target_img, middle_center=True, offset=(0, -TILE_PIXEL * 3))
            return info_bg
        
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
        ## Finish Condition
            1. Select the correct item. (reward: 1)
            2. Select the wrong item. (reward: 0)
        """
        reward, terminate = False, False
        
        bag_obj = self.bag.objs[0]
        if bag_obj:
            terminate = True
            if hasattr(bag_obj, "related_name") and bag_obj.related_name == self.target_obj.name:
                reward = True
        return reward, terminate
