import os
from src.utils import *
from src.config import *


class Obj:
    def __init__(self, 
                 name: str,
                 type: str,
                 tile: int = TILE_PIXEL,
                 c_pk: bool = False, 
                 id: int = None, 
                 pos: tuple = None, 
                 **kwargs):
        """
        params:
            name: the name of the obj
            type: the type of the obj
            c_pk: whether the obj can be picked
            id: the id of the obj
            pos: the position of the obj, (x, y)
            kwargs: other optional attributes
        """
        
        self.name = name    
        self.type = type
        self.c_pk = c_pk
        self.id = id
        self.pos = pos
        self.tile = tile
        obj_img_path = os.path.join(IMG_BASE_PATH, f"{self.type}/{self.name}.png") 
        self.img = LoadImage(obj_img_path, 96)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_id(self, id: int):
        """
        Set the id of the obj.
        """
        self.id = id

    def set_pos(self, pos: tuple):
        """
        Set the position of the obj.
        """
        self.pos = pos 
        
    def set_attr(self, attr: str, value):
        """
        Set the attribute of the obj, add or change.
        """
        setattr(self, attr, value)    
    
    def get_attr(self, attr: str):
        """
        Get the attribute of the obj, if not exist, return False.
        """
        if hasattr(self, attr):
            return getattr(self, attr)
        return False

    def __str__(self):
        return f"Obj: {self.__dict__}"
    
    def render(self, obj_px = TILE_PIXEL, id_px = ID_IMG_PIXEL, show_id = False):
        """
        Render the image of the obj.
        """
        
        # original image
        obj_img_path = os.path.join(IMG_BASE_PATH, f"{self.type}/{self.name}.png") 
        assert os.path.exists(obj_img_path), f"Obj image not found: {obj_img_path}"
        obj_img = LoadImage(obj_img_path, tile_px = self.tile)
        if not show_id:
            return obj_img
        
        # add id image at bottom center
        if self.id != None:
            id_img_path = os.path.join(OBJ_ID_IMG_PATH, f"{self.id}.png")
            # assert os.path.exists(id_img_path), f"ID image not found: {id_img_path}"
            id_img = LoadImage(id_img_path, tile_px = id_px)
            combined_img = None
            if not hasattr(self, "visible") or self.visible == True:
                combined_img = ImgOverlay(obj_img, id_img, offset = ((obj_px - id_px) // 2, obj_px - id_px))
            return combined_img
        return obj_img
