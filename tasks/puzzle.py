from src.obj import Obj
from src.task import KidGymTask
from src.config import *
from src.utils import *

class Puzzle(KidGymTask):
    """
    ## Description
    A target image composed of four puzzle pieces is displayed in the 
    hint bar, and the agent needs to assemble the scattered puzzle pieces
    from its backpack to reconstruct the target image.
    
    """
    def __init__(self, 
                 match_pieces: int = 1,
                 **kwargs):
        """
        match_pieces: The number of missing pieces needed to be resorted. (default: 1)
        
        Level 1: match_pieces = 1
        Level 2: match_pieces = 2
        Level 3: match_pieces: = 3
        """
        super().__init__(**kwargs)
        self.match_pieces = match_pieces
        self.target_pos = []
        self.grid.gen_rule = [[0, 0, 0, 0, 0],
                [0, 1, 3, 0, 0],
                [0, 2, 4, 0, 0],
                [0, 0, 0, 'A', 0],
                [0, 0, 0, 0, 0]]
        self.grid.show_id = False
        self.side_bar = True

    def generate_scene_and_goal(self):
        """
        Generate the game based on the task.
        """
        self.type = PUZZLE_TYPE
        self.correct_num = 0
        roman = RESOURCE["roman"]["resources"][:4]
        pieces = RESOURCE["tool"]["puzzle"]
        self.missing = random.sample([0, 1, 2, 3], self.match_pieces)
        pos = 0
        self.pieces = []

        random.shuffle(pieces)
        for i in range(len(pieces)):
            obj = Obj(pieces[i], "toy", position_id = i + 1, correct_id = i + 1)
            self.pieces.append(obj)
            if i in self.missing:
                obj = Obj(roman[pos], "roman", position_id = i + 1)
                self.grid.add_obj(obj)
                pos += 1
            else:
                self.grid.add_obj(obj)
        
        img12 = ImgCombine(self.pieces[0].img, self.pieces[1].img, pad_h=False)
        img34 = ImgCombine(self.pieces[2].img, self.pieces[3].img, pad_h=False)
        self.target = ImgZoom(ImgCombine(img12, img34, pad_h=True), factor=0.6)
        
        random.shuffle(self.pieces)
        for piece in self.pieces:
            self.bag.add(piece)
        
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
            1. choose item number {obj_id}
        """
        
        action_templates = self.get_template()["action"]
        
        actions = []
        selections = 'ABCD'
        for i in range(self.bag.num):
            for j in range(self.bag.num):
                if not hasattr(self.grid.objs[j], 'correct_id'):
                    action_template = action_templates["place_piece"]
                    action = FillTemplate(action_template, {"backpack_id": selections[i], "symbol": self.grid.objs[j].name})
                    actions.append(action)  
        
        random.shuffle(actions)
        return actions
    
    def get_info_img(self):
        info_bg = np.ones((TILE_PIXEL * 9, TILE_PIXEL * 2, 4), dtype = np.uint8) * 255
        target_img = ImgOverlay(ImgZoom(LoadImage(f"{IMG_BASE_PATH}/game/bag_grid.png"), 1.1), ImgZoom(self.target, 0.75), middle_center=True)
        info_img = ImgOverlay(info_bg, target_img, middle_center=True)
        
        return info_img
    
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
        if hasattr(bag_obj, 'correct_id') and bag_obj.correct_id == target_obj.position_id:
            self.correct_num += 1

        return actions
    
    def check_grid(self) -> bool:
        return True

    def check_goal(self) -> tuple[bool, bool]:
        """
        ## Finish Condition
            1. Place the correct piece in the blank frame. (reward: 1)
            2. Place the wrong piece in the blank frame. (reward: 0)
        """
        num = 0
        for obj in self.bag.objs:
            if obj:
                num += 1
        if num != 4 - self.match_pieces:
            return False, False
        
        if self.correct_num == self.match_pieces:
            return True, True
        
        return False, True
