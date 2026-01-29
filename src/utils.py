from collections import deque
import heapq
import random
import re
import numpy as np
from PIL import Image
from src.config import *

def LoadImage(path: str, tile_px: int = None) -> np.ndarray:
    """
    Use PIL to load, convert to 4 channels np.ndarray.
    """
    img = Image.open(path).convert("RGBA")
    # keep original size
    if tile_px is None:
        return PIL2np(img)
    # if tile_px, resize to *SQUARE* size(tile_px, tile_px)
    return ImgResize(img, tile_px)

def SaveImage(img: np.ndarray | Image.Image, path: str = "test.png"):
    """ 
    Use PIL to save image.
    """
    if isinstance(img, np.ndarray):
        img = np2PIL(img)
    assert isinstance(img, Image.Image), "img type should be *PIL.Image*"
    img.save(path)

def PIL2np(pil_img: Image.Image) -> np.ndarray:
    """
    Convert PIL image to numpy array.
    """
    assert isinstance(pil_img, Image.Image), "Img type should be PIL.Image."
    return np.array(pil_img)

def np2PIL(img: np.ndarray) -> Image.Image:
    """
    Convert numpy array to PIL image.
    """
    assert isinstance(img, np.ndarray), "Img type should be np.ndarray."
    return Image.fromarray(img)

def ImgResize(img: np.ndarray | Image.Image, size: int) -> np.ndarray:
    """
    Resize the original *SQAURE* image into the specified size.
    """
    if isinstance(img, np.ndarray):
        img = np2PIL(img)
    resized_img = img.resize((size, size), Image.LANCZOS)
    return PIL2np(resized_img)

def ImgZoom(img: np.ndarray | Image.Image, factor: float = 1.0) -> np.ndarray:
    """
    Zoom in or out the original square image with the specified factor.
    """
    if isinstance(img, np.ndarray):
        img = np2PIL(img)
    size = img.size
    resized_img = img.resize((int(size[0] * factor), int(size[1] * factor)), Image.LANCZOS)
    return PIL2np(resized_img)

def ImgOverlay(bg_img: np.ndarray, fg_img: np.ndarray, offset: tuple = (0, 0), top_center: bool = False,
               bottom_center: bool = False, middle_center: bool = False,) -> np.ndarray:
    """
    Overlay a foreground image on a background image.
    Keep the non-transparent pixels of the foreground image.
    reference: https://blog.csdn.net/joyce_peng/article/details/114123335
    """
    
    if fg_img is None:
        return bg_img
    
    # Convert numpy arrays to PIL images and ensure they are in RGBA mode
    bg_img_PIL = np2PIL(bg_img).convert('RGBA')
    fg_img_PIL = np2PIL(fg_img).convert('RGBA')

    bg_h, bg_w = bg_img.shape[0], bg_img.shape[1]
    fg_h, fg_w = fg_img.shape[0], fg_img.shape[1]
        
    # adjust offset
    offset_ = (0, 0)
    if top_center:
        offset = ((bg_w - fg_w) // 2, 0)
    elif bottom_center:
        offset_ = ((bg_w - fg_w) // 2, bg_h - fg_h)
    elif middle_center:
        offset_ = ((bg_w - fg_w) // 2, (bg_h - fg_h) // 2)    
    offset_ = (offset_[0] + offset[0], offset_[1] + offset[1])
    
    # Paste the foreground image onto the background at the specified position
    bg_img_PIL.paste(fg_img_PIL, offset_, mask=fg_img_PIL)
    return PIL2np(bg_img_PIL.convert('RGBA'))

def ImgsCombine(imgs: list[np.ndarray], pad_h: bool = True, padding: int = 0) -> np.ndarray:
    """
    Combine multiple images into one.
    If the width/height is different, fill with white.
    pad_h(True): |
                 |
    pad_h(False): ----
    """
    if len(imgs) == 0:
        return None
    
    combined_img = imgs[0]
    for img in imgs[1:]:
        combined_img = ImgCombine(combined_img, img, pad_h, padding)
    
    return combined_img

def ImgCombine(img_1: np.ndarray, img_2: np.ndarray, pad_h: bool = True, padding: int = 0) -> np.ndarray:
    """
    Combine two images into one.
    """
    h1, w1, chs1 = img_1.shape
    h2, w2, chs2 = img_2.shape
    
    # padding h
    if pad_h:
        max_width = max(w1, w2)
        img_1 = np.pad(img_1, ((0, 0), (0, max_width - w1), (0, 0)), mode = 'constant', constant_values = 255)
        img_2 = np.pad(img_2, ((0, 0), (0, max_width - w2), (0, 0)), mode = 'constant', constant_values = 255)
        padding_img = np.ones((padding, max_width, chs1), dtype=np.uint8) * 255
        # combine
        combined_img = np.zeros((h1 + h2 + padding, max_width, chs1), dtype = np.uint8)
        combined_img[:h1, :, :] = img_1
        combined_img[h1:h1+padding, :, :] = padding_img
        combined_img[h1+padding:, :, :] = img_2
    
    # padding w
    else:
        max_height = max(h1, h2)
        img_1 = np.pad(img_1, ((0, max_height - h1), (0, 0), (0, 0)), mode = 'constant', constant_values = 255)
        img_2 = np.pad(img_2, ((0, max_height - h2), (0, 0), (0, 0)), mode = 'constant', constant_values = 255)
        padding_img = np.ones((max_height, padding, chs1), dtype=np.uint8) * 255
        # combine
        combined_img = np.zeros((max_height, w1 + w2 + padding, chs1), dtype = np.uint8)
        combined_img[:, :w1, :] = img_1
        combined_img[:, w1:w1+padding, :] = padding_img
        combined_img[:, w1+padding:, :] = img_2
    
    return combined_img

def ImgFill(bg_img: np.ndarray, fg_img: np.ndarray, x: int, y: int, tile_px: int, 
            new_size: tuple = None, offset: tuple[int, int] = (0, 0)) -> np.ndarray:
    """
    Fill the background image with the foreground image at (x, y).
    """ 
    if fg_img is None:
        return bg_img
    y_start = y * tile_px + offset[1]
    x_start = x * tile_px + offset[0]
    
    if new_size:
        y_start = y * new_size[0] + offset[1]
        x_start = x * new_size[1] + offset[0]
        # print(fg_img.shape, new_size, y_start, x_start)
        bg_img[y_start : y_start + new_size[0], x_start : x_start + new_size[1]] = fg_img
    else:
        y_start = y * tile_px + offset[1]
        x_start = x * tile_px + offset[0]
        bg_img[y_start : y_start + tile_px, x_start : x_start + tile_px] = fg_img
    return bg_img

def RandomChoose(elements: list, num: int = 1, exclude: list = None) -> list:
    """
    Randomly choose n elements from a list, avoiding elements in the ban list.
    
    Parameters:
    elements (list): List of elements to choose from.
    num (int): Number of elements to randomly choose. Defaults to 1.
    exclude (list): List of elements to avoid. Defaults to None.
    
    Returns:
    list: List of randomly chosen elements, or a single element if num == 1.
    """
    if exclude is None:
        exclude = []
    elif not isinstance(exclude, list):
        exclude = [exclude]
    
    # Filter out excluded elements from the list
    available_elements = [e for e in elements if e not in exclude]
    
    # If there are fewer available elements than requested, handle appropriately
    if len(available_elements) < num:
        raise ValueError("Not enough available elements to choose from.")
    
    # Shuffle the available elements
    random.shuffle(available_elements)
    
    # Return the appropriate number of elements
    return available_elements[0] if num == 1 else available_elements[:num]

def FillTemplate(template: str, values: dict) -> str:
    """
    Fill the template string with values from the dictionary.
    """
    return template.format(**values)

def DecodeFirstNumber(instruction: str) -> int:
    """
    Decode the number in the instruction.
    """
    return int(re.findall(r'[0123456789]', instruction)[0])

def DecodeFirstLetter(instruction: str) -> str:
    """
    Decode the letter in the instruction.
    """
    return re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', instruction)[0]

def DecodeFirstRoman(instruction: str) -> str:
    """
    Decode the roman number in the instruction.
    """
    return re.findall(r'\b(IX|VIII|VII|VI|V|IV|III|II|I)\b', instruction)[0]

def a_star_search(grid, start, goal):
    start = start[::-1]
    goal = goal[::-1]
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # 曼哈顿距离

    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 上下左右四个方向
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    open_set = []
    heapq.heappush(open_set, (fscore[start], start))
    while open_set:
        current = heapq.heappop(open_set)[1]

        # 如果当前节点是目标节点，重建路径
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j

            # 检查是否在网格范围内
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]):
                # 检查障碍物
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue

                tentative_g_score = gscore[current] + 1

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in open_set]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (fscore[neighbor], neighbor))

    return False  # 如果无法找到路径

def ExtractPath(path, tar_pos, agent_dir):
    # ensure path exists
        if path is None:
            return None
        assert len(path) >= 2, "path length should be at least 2"
        
        action_queue = deque()
        # translate x,y change to actions
        for i in range(1, len(path) - 1):
            x_change = path[i][0] - path[i - 1][0]
            y_change = path[i][1] - path[i - 1][1]
            # TODO: action id
            action_queue.append(ACTION(POS_TO_DIR[(y_change, x_change)]))

        # pay attention to x,y order
        # need to move at least 1 step and then rotate
        if len(path) >= 3:
            tar_pos = tar_pos[::-1]
            last_pos_2 = path[-2]
            last_pos_3 = path[-3]
            cur_dir = POS_TO_DIR[(last_pos_2[1] - last_pos_3[1], last_pos_2[0] - last_pos_3[0])]
            goal_dir = POS_TO_DIR[(tar_pos[1] - last_pos_2[1], tar_pos[0] - last_pos_2[0])]
            while cur_dir != goal_dir:
                action_queue.append(ACTION.ROTATE)
                cur_dir = (cur_dir - 1) % 4

        # no need to move, only rotate
        else:
            tar_pos = tar_pos[::-1]
            last_pos_2 = path[-2]
            cur_dir = agent_dir
            goal_dir = POS_TO_DIR[(tar_pos[1] - last_pos_2[1], tar_pos[0] - last_pos_2[0])]
            while cur_dir != goal_dir:
                action_queue.append(ACTION.ROTATE)
                cur_dir = (cur_dir - 1) % 4
        
        return action_queue