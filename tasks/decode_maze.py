from pickle import NONE
from re import T
from tkinter import N
from src.obj import Obj
from src.task import KidGymTask
from src.config import *
from src.utils import *
import json

class DecodeMaze(KidGymTask):
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
        self.side_bar = True
        with open(f'{JSON_PATH}/{self.name}_L{self.level}.json', 'r') as file:
            self.data = json.load(file)

    def generate_scene_and_goal(self):
        """
        Generate the game based on the task.
        """
        self.grid.gen_rule = self.data[f"{self.iter}"]

        self.type = SEQUENCE_TYPE

        diamond = "diamond"
        keys = RESOURCE["tool"]["key"]
        doors = RESOURCE["tool"]["door"]
        wall = RESOURCE["maze"]["resources"]

        random_keys = keys
        random_doors = [doors[2], doors[0], doors[1]]

        self.keys = []
        self.doors = []

        random_i = random.randint(0, 3)

        for i in range(self.match_pairs):
            j = (i + random_i) % 3
            key = Obj(random_keys[j], "key", c_pk=True, position_id = 2 )
            door = Obj(random_doors[j], "door", c_op=random_keys[j], position_id = 3 )
            self.keys.append(key)
            self.doors.append(door)
            self.grid.add_obj(key)
            self.grid.add_obj(door)

        if self.match_pairs == 1:
            self.grid.add_obj(Obj(keys[(j + 2) % 3], "key", c_pk=True, position_id = 2))

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
    
    def get_info_img(self):
        def render_decode_relationship(obj_1: Obj, obj_2: Obj):
            white_bg = np.ones((TILE_PIXEL, TILE_PIXEL, 4), dtype = np.uint8) * 255
            obj_1_img = ImgOverlay(white_bg, ImgZoom(obj_1.img, 0.5), middle_center=True)
            obj_2_img = ImgOverlay(white_bg, ImgZoom(obj_2.img, 0.5), middle_center=True)
            # combine two obj imgs and add arrow
            arrow_img = LoadImage(f"{IMG_BASE_PATH}/game/arrow.png")
            relationship_img = ImgOverlay(ImgCombine(obj_1_img, obj_2_img, pad_h=False), ImgZoom(arrow_img, 0.2), middle_center=True)
            return relationship_img

        def render_decode_relationships(objs_1: list[Obj], objs_2: list[Obj]):
            if self.match_pairs == 1:
                return render_decode_relationship(objs_1[0], objs_2[0])
            else:
                relationship_imgs = []
                for i in range(self.match_pairs):
                    relationship_imgs.append(render_decode_relationship(objs_1[i], objs_2[i]))
                # random.shuffle(relationship_imgs)
                relationship_table_img = relationship_imgs[0]
                for i in range(1, len(relationship_imgs)):
                    relationship_table_img = ImgCombine(relationship_table_img, relationship_imgs[i], pad_h=True)
                return relationship_table_img
            
        render_table_fg = render_decode_relationships(self.keys, self.doors)
        info_bg = np.ones((TILE_PIXEL * 9, TILE_PIXEL * 2, 4), dtype = np.uint8) * 255
        info_bg = ImgOverlay(info_bg, render_table_fg, middle_center=True)
        # SaveImage(info_bg, "1.png")
        return info_bg

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


# if __name__ == "__main__":


#     for mp in range(2, 4):

#         grids = {}

#         task = DecodeMaze(match_pairs = mp, task_name = f"Decode_Maze_L{mp}")

#         for i in range(100):
#             # task.reset()

#             task.generate_game()
#             valid, grid = task.check_grid()
#             # # print(grid)
#             grid = grid.T.tolist()

#             for row in grid:
#                 for j in range(len(row)):
#                     if row[j] == -1:
#                         row[j] = "A"

#             grids[f"{i+1}"] = grid

#             task.save_obs(path="decode_maze.png")


#         with open(f"Decode_Maze_L{mp}.json", "w") as f:
#             json.dump(grids, f, indent=4)
