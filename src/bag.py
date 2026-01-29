
import os
from src.utils import *
from src.config import *

class Bag:
    def __init__(self, size: int = 4):
        """
        params:
            size: the size of the bag
            num: the number of objs in the bag(0 <= num <= size)
            objs: the objs in the bag
        """
        self.size = size
        self.reset()
    
    def reset(self):
        """
        Reset the bag, clear all objects.
        """
        self.num = 0
        self.objs = [None] * self.size

    @property
    def empty(self) -> bool:
        """
        Check whether the bag is empty.
        """
        return self.num == 0

    @property
    def full(self) -> bool:
        """
        Check whether the bag is full.
        """
        return self.num == self.size
    
    def add(self, obj) -> bool:
        """
        Add a new obj to the bag.
        If the bag is full, return False, o.w. True.
        """
        if self.full:
            return False
        
        self.objs[self.num] = obj
        self.num += 1
        return True

    def get(self, idx: int = 0):
        """
        Get the object at specific index.
        If the index is out of range, return None.
        """
        if idx < 0 or idx >= self.size:
            return None
        return self.objs[idx]

    def remove(self, idx: int = 0):
        """
        Remove the obj at specific index.
        If the index is out of range, return None.
        """
        obj = self.get(idx)
        if obj is None:
            return None
        
        self.objs = self.objs[:idx] + self.objs[idx+1:] + [None]
        self.num -= 1
        return obj

    def __str__(self):
        return f"Bag({self.num}/{self.size}): [{', '.join(str(obj.name) for obj in self.objs if obj is not None)}]"
     
    def render(self):
        """
        Render the whole bag.
        """
        bag_bg_size = (TILE_PIXEL, 448)
        bag_bg = np.ones((*bag_bg_size, 4), dtype=np.uint8) * 255
        render_imgs = []
        for idx in range(self.size):
            render_imgs.append(self.renderSingle(idx))
        bag_fg = ImgsCombine(render_imgs, pad_h = False, padding = BAG_IMG_PADDING)
        # TODO: simplify the code
        combnined_img = ImgOverlay(bag_bg, bag_fg, bottom_center = True)
        return combnined_img
        
    def renderSingle(self, idx: int):
        """
        Render the object at specific index.
        """
        border_img_path = os.path.join(BAG_ID_IMG_PATH, f"{NUMBER_TO_LETTER[idx]}.png")
        border_img = LoadImage(border_img_path)
        
        # blank bag
        obj = self.get(idx)
        if obj is None:
            return border_img
        
        # obj in bag
        obj_img = obj.render(show_id = False)
        combined_img = ImgOverlay(border_img, ImgZoom(obj_img, 0.8), middle_center=True, offset = BAG_IMG_OFFSET)
        return combined_img
            