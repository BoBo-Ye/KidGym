import os
from src.bag import Bag
from src.utils import *
from src.config import *

class Agent:
    def __init__(self, bag_size: int = BAG_SIZE):
        """
        params:
            bag_size: the size of the bag
            pos: the position of the agent, (x, y)
            dir: the direction of the agent, 0-3
        """
        self.bag = Bag(bag_size)
        self.reset()
    
    def reset(self, pos: tuple = (0, 0), dir: int = 0):
        """
        Reset the agent, clear the bag.
        """
        self.pos = pos
        self.dir = dir
        self.bag.reset()

    def set_pos(self, pos: tuple = None):
        """
        Set the agent's position.
        """
        self.pos = pos

    def set_dir(self, dir: int):
        """
        Set the agent's direction.
        0: down, 1: right, 2: up, 3: left
        """
        while self.dir != dir:
            self.rotate()
            
    def get_next_pos(self) -> tuple:
        """
        Get the next position of the agent based on the direction.
        """
        return (self.pos[0] + DIR_TO_POS[self.dir][0], self.pos[1] + DIR_TO_POS[self.dir][1])
    
    def rotate(self):
        """
        Rotate 90 degrees *CLOCKWISE*.
        """
        self.dir = (self.dir - 1) % 4

    def get(self, idx: int = 0):
        """
        Get the object at specific index from the bag.
        If the index is out of range, return None.
        """
        return self.bag.get(idx)
    
    def pick(self, obj):
        """
        Pick the object from the grid to the bag.
        """
        # pos becomes None
        obj.set_pos(None)
        self.bag.add(obj)
        
    def drop(self, idx: int = 0, pos: tuple = None):
        """
        Drop the object from the bag to the grid.
        """
        obj = self.bag.remove(idx)
        if obj:
            obj.set_pos(pos)
        return obj
    
    def render(self, px = TILE_PIXEL):
        """
        Render the image of the obj.
        """
        agent_img = LoadImage(AGENT_IMG_PATH, tile_px = px)
        dir_img_path = os.path.join(AGENT_DIR_IMG_PATH, f"direction_{self.dir}.png")
        dir_img = LoadImage(dir_img_path, tile_px = px)
        combined_img = ImgOverlay(agent_img, dir_img)
        return combined_img
    