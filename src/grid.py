import copy
import random
import numpy as np
from src.obj import Obj
from src.agent import Agent
from src.utils import *
from src.config import *

class Grid:
    def __init__(self,
                 size: int = GRID_SIZE,
                 bag_size: int = BAG_SIZE,
                 tile_px: int = TILE_PIXEL):
        
        """
        size: the size of the grid
        bag_size: the size of the bag
        tile_px: the pixel size of the tile
        """
        self.size = size
        self.tile_px = tile_px
        self.agent = Agent(bag_size)
        self.objs = []
        self.gen_rule = None
        self.show_id = True
        
    def reset(self):
        """
        Clear the objs and reset agent.
        """
        self.objs.clear()
        self.agent.reset()

    def add_obj(self, obj: Obj, num: int = 1):
        """
        Add object(s) to the grid.
        """
        for _ in range(num):
            copy_obj = copy.deepcopy(obj) # need deep copy, or the objs are the same
            self.objs.append(copy_obj)
        
    def get_obj_with_pos(self, x: int, y: int):
        """
        Return the obj at (x, y).
        """
        if not self.in_grid(x, y):
            return None
        
        for obj in self.objs:
            if obj.pos == (x, y):
                return obj
        return None

    def get_obj_with_id(self, id: int):
        """
        Get the the object with the given id.
        """
        for obj in self.objs:
            if obj.id == id:
                return obj
        return None
    
    def get_obj_with_name(self, name: str):
        """
        Get the the object with the given name.
        """
        for obj in self.objs:
            if obj.name == name:
                return obj
        return None

    def in_grid(self, x: int, y: int) -> bool:
        """
        Check whether (x,y) is in the grid range.
        """
        return 0 <= x < self.size and 0 <= y < self.size
        
    def can_move(self, x: int, y: int) -> bool:
        """
        Check whether the agent can move to (x,y).
        """
        obj = self.get_obj_with_pos(x, y)
        return (obj is None) and self.in_grid(x, y)
    
    def try_move(self, dir: int) -> bool:
        """
        Try to make agent move to the next given direction grid.
        """
        self.agent.set_dir(dir)
        new_pos = self.agent.get_next_pos()
        if self.can_move(*new_pos):
            self.agent.set_pos(new_pos)
            return True
        return False

    def try_rotate(self) -> bool:
        """
        Try to make agent rotate 90 clockwise. Always success.
        """
        self.agent.rotate()
        return True
    
    def try_pick(self) -> bool:
        """
        Try to make agent pick the front object.
        """
        pick_pos = self.agent.get_next_pos()
        obj = self.get_obj_with_pos(*pick_pos)
        if obj is None or not obj.c_pk:
            return False
        self.agent.pick(obj)
        self.objs.remove(obj)
        return True
    
    def try_drop(self, idx: int) -> bool:
        """
        Try to make agent drop the front object.
        """
        obj = self.agent.get(idx)
        drop_pos = self.agent.get_next_pos()
        if obj is None or not self.can_move(*drop_pos): # TODO: can_move is not the best judgement(can_drop?)
            return False
        drop_obj = self.agent.drop(idx, drop_pos)
        self.objs.append(drop_obj)
        return True

    def render(self):
        """
        Render the image of the whole grid.
        """
        frame_px = self.size * self.tile_px
        frame = np.zeros((frame_px, frame_px, 4), dtype=np.uint8)
        
        for obj in self.objs:
            obj_img = obj.render(self.tile_px, show_id = self.show_id)
            frame = ImgFill(frame, obj_img, obj.pos[0], obj.pos[1], self.tile_px)
            
        agent_img = self.agent.render(self.tile_px)
        frame = ImgFill(frame, agent_img, self.agent.pos[0], self.agent.pos[1], self.tile_px)
        return frame
    
    def gen_random_scene(self):
        """
        Assign random ids and positions to the objects.
        """
        self.gen_random_id()
        if self.gen_rule == None:
            self.gen_random_pos()
        else:
            self.gen_ruled_pos()
    
    def gen_random_id(self):
        """
        Generate random ids for the objects.
        """
        random.shuffle(self.objs)
        i = 0
        for obj in self.objs:
            if obj.name != "wall":
                obj.set_id(i)
                i += 1

    def gen_random_pos(self):
        """
        Generate a random map with objects.
        """
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(positions)
        # set agent position
        self.agent.set_pos(positions.pop())
        # set objs positions
        for obj in self.objs:
            obj.set_pos(positions.pop())
            
    def gen_ruled_pos(self):
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(positions)
        for obj in self.objs:
            if hasattr(obj, "position_id"):
                can_assign = [(i, j) for i in range(self.size) for j in range(self.size) \
                          if (i, j) in positions and obj.position_id == self.gen_rule[i][j]]
                assert can_assign, f"No valid positions available!"
                random.shuffle(can_assign)
                pos = can_assign.pop()
                obj.set_pos(pos)
                positions.remove(pos)
        
        for obj in self.objs:
            if not hasattr(obj, "position_id"):
                obj.set_pos(positions.pop())
                
        random.shuffle(positions)
        if self.agent is not None:
            for i in range(len(self.gen_rule)):  # i 是行
                for j in range(len(self.gen_rule[i])):  # j 是列
                    if self.gen_rule[i][j] == 'A':
                        self.agent.set_pos((i, j))
                        return
        self.agent.set_pos(positions.pop())
                
    def construct_map(self):
        """
        Construct the grid move map.
        0 - can move
        1 - cannot move
        """
        grid_map = np.zeros((self.size, self.size), dtype = np.uint8)
        for obj in self.objs:
            grid_map[obj.pos[1], obj.pos[0]] = 1
        return grid_map
            
    def search_path(self, target_pos: tuple):
        """
        Search the path from agent to target_pos.
        """
        grid_map = self.construct_map()
        # set agent and target position to 0(can move)
        grid_map[self.agent.pos[1], self.agent.pos[0]] = 0
        grid_map[target_pos[1], target_pos[0]] = 0
        # use a* search to find the path
        path = a_star_search(grid_map, self.agent.pos, target_pos)
        # print(path)
        return path
    
    def extract_path(self, target_pos: tuple):
        """
        Extract the path to actions list from agent to target_pos.
        """
        path = self.search_path(target_pos)
        if not path or len(path) == 1:
            return []
        return ExtractPath(path, target_pos, self.agent.dir)