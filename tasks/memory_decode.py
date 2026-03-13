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
        obj = Obj(related_obj, objs_2_type, position_id = 2, c_pk=True, related_name = target_obj, visible = False)
        self.grid.add_obj(obj)
        
        exclude=[target_obj, related_obj]
        for _ in range(self.related_num * 2 + 1):
            type = RandomChoose(TYPES)
            new_obj = RandomChoose(RESOURCE[type]["resources"], 1, exclude)
            obj = Obj(new_obj, type, position_id = 2, c_pk=True, visible = False)
            self.grid.add_obj(obj)
            exclude.append(new_obj)
            
        self.goal = self.get_template()["goal"]
            
        return self.goal
        
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
  
    def get_info_img(self):
        def render_decode_relationship(obj_1: Obj, obj_2: Obj):
            # copy transparent fg_img to white bg
            white_bg = np.ones((TILE_PIXEL, TILE_PIXEL, 4), dtype = np.uint8) * 255
            obj_1_img = ImgOverlay(white_bg, ImgZoom(obj_1.img, 0.5), middle_center=True)
            obj_2_img = ImgOverlay(white_bg, ImgZoom(obj_2.img, 0.5), middle_center=True)
            # combine two obj imgs and add arrow
            arrow_img = LoadImage(f"{IMG_BASE_PATH}/game/arrow.png")
            relationship_img = ImgOverlay(ImgCombine(obj_1_img, obj_2_img, pad_h=False), ImgZoom(arrow_img, 0.2), middle_center=True)
            return relationship_img
    
        def render_decode_relationships(objs_1: list[Obj], objs_2: list[Obj]):
            if self.related_num == 1:
                relationship_img = render_decode_relationship(objs_1, objs_2)
                return relationship_img
            relationship_imgs = []
            for obj_1, obj_2 in zip(objs_1, objs_2):
                relationship_imgs.append(render_decode_relationship(obj_1, obj_2))
            # combine all relationship imgs into a table
            relationship_table_img = relationship_imgs[0]
            for i in range(1, len(relationship_imgs)):
                relationship_table_img = ImgCombine(relationship_table_img, relationship_imgs[i], pad_h = True)
            return relationship_table_img

        if self.cur_step == 0:
            render_table_fg = render_decode_relationships(self.objs_1, self.objs_2)
            info_bg = np.ones((TILE_PIXEL * 9, TILE_PIXEL * 2, 4), dtype = np.uint8) * 255
            info_bg = ImgOverlay(info_bg, render_table_fg, middle_center=True)
            return info_bg
        else:
            # self.side_bar = False
            for obj in self.grid.objs:
                if obj.position_id == 2:
                    obj.visible = True
            
            self.goal = self.get_template()["goal_1"]
            info_bg = np.ones((TILE_PIXEL * 9, TILE_PIXEL * 2, 4), dtype = np.uint8) * 255
            render_table_fg = render_decode_relationships(self.objs_1, self.objs_2)        
            target_img = ImgOverlay(ImgZoom(LoadImage(f"{IMG_BASE_PATH}/game/bag_grid.png"), 1.1), ImgZoom(self.target_obj.img, 0.9), middle_center=True)
            info_bg = ImgOverlay(info_bg, target_img, middle_center=True)
            return info_bg
        
