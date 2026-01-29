from gymnasium.envs.registration import register

TASK_NAMES = [
    "CL_L1", "CL_L2", "CL_L3",
    "PU_L1", "PU_L2", "PU_L3",
    "CO_L1", "CO_L2", "CO_L3",
    "PL_L1", "PL_L2", "PL_L3",
    "SO_L1", "SO_L2", "SO_L3",
    "FI_L1", "FI_L2", "FI_L3",
    "MA_L1", "MA_L2", "MA_L3",
    "DE_L1", "DE_L2", "DE_L3",
    "SE_L1", "SE_L2", "SE_L3",
    "MMA_L1", "MMA_L2", "MMA_L3",
    "MFI_L1", "MFI_L2", "MFI_L3",
    "MDE_L1", "MDE_L2", "MDE_L3", 
]

def REGISTER_TASKS():
    register(
        id = 'CL_L1',
        entry_point = 'tasks.classification:Classification',
        kwargs = {'type_num': 2, 'item_num': 1, 'max_steps': 4, 
                  'high_level': True, 'task_name': 'Classification_L1'}
    )

    register(
        id = 'CL_L2',
        entry_point = 'tasks.classification:Classification',
        kwargs = {'type_num': 2, 'item_num': 2, 'max_steps': 8, 
                  'high_level': True, 'task_name': 'Classification_L2'}
    )
        
    register(
        id = 'CL_L3',
        entry_point = 'tasks.classification:Classification',
        kwargs = {'type_num': 2, 'item_num': 3, 'max_steps': 12,
                  'high_level': True, 'task_name': 'Classification_L3'}
    )

    register(
        id = 'PU_L1',
        entry_point = 'tasks.puzzle:Puzzle',
        kwargs = {'match_pieces' : 1, 'max_steps': 1, 
                  'high_level': True, 'task_name': 'Puzzle_L1'}
    )

    register(
        id = 'PU_L2',
        entry_point = 'tasks.puzzle:Puzzle',
        kwargs = {'match_pieces' : 2, 'max_steps': 2, 
                  'high_level': True, 'task_name': 'Puzzle_L2'}
    )

    register(
        id = 'PU_L3',
        entry_point = 'tasks.puzzle:Puzzle',
        kwargs = {'match_pieces' : 3, 'max_steps': 3, 
                  'high_level': True, 'task_name': 'Puzzle_L3'}
    )

    register(
        id = 'CO_L1',
        entry_point = 'tasks.counting:Counting',
        kwargs = {'type_num': 1, 'range': (1, 3), 'max_steps': 5, 
                  'high_level': True, 'task_name': 'Counting_L1'}
    )

    register(
        id = 'CO_L2',
        entry_point = 'tasks.counting:Counting',
        kwargs = {'type_num': 2, 'range': (2, 6), 'max_steps': 5, 
                  'high_level': True, 'task_name': 'Counting_L2'}
    )

    register(
        id = 'CO_L3',
        entry_point = 'tasks.counting:Counting',
        kwargs = {'type_num': 3, 'range': (3, 9), 'max_steps': 5, 
                  "high_level": True, 'task_name': 'Counting_L3'}
    )

    register(
        id = 'PL_L1',
        entry_point = 'tasks.placement:Placement',
        kwargs = {'level' : 1, 'max_steps': 1, 
                  'high_level': True, 'task_name': 'Placement_L1'}
    )

    register(
        id = 'PL_L2',
        entry_point = 'tasks.placement:Placement',
        kwargs = {'level' : 2, 'max_steps': 1, 
                  'high_level': True, 'task_name': 'Placement_L2'}
    )
        
    register(
        id = 'PL_L3',
        entry_point = 'tasks.placement:Placement',
        kwargs = {'level' : 3, 'max_steps': 1, 
                  'high_level': True, 'task_name': 'Placement_L3'}
    )
           
    register(
        id = 'SO_L1',
        entry_point = 'tasks.sorting:Sorting',
        kwargs = {'related_num': 2, 'max_steps': 2,
                  'high_level': True, 'task_name': 'Sorting_L1'}
    )

    register(
        id = 'SO_L2',
        entry_point = 'tasks.sorting:Sorting',
        kwargs = {'related_num': 3, 'max_steps': 3,
                  'high_level': True, 'task_name': 'Sorting_L2'}
    )

    register(
        id = 'SO_L3',
        entry_point = 'tasks.sorting:Sorting',
        kwargs = {'related_num': 4, 'max_steps': 4,
                  'high_level': True, 'task_name': 'Sorting_L3'}
    )

    register(
        id = 'FI_L1',
        entry_point = 'tasks.filling:Filling',
        kwargs = {'match_pieces' : 1, 'max_steps': 1,
                  'high_level': True, 'task_name': 'Filling_L1'}
    )

    register(
        id = 'FI_L2',
        entry_point = 'tasks.filling:Filling',
        kwargs = {'match_pieces' : 2, 'max_steps': 2,
                  'high_level': True, 'task_name': 'Filling_L2'}
    )
    
    register(
        id = 'FI_L3',
        entry_point = 'tasks.filling:Filling',
        kwargs = {'match_pieces' : 3, 'max_steps': 3,
                  'high_level': True, 'task_name': 'Filling_L3'}
    )

    register(
        id = 'MA_L1',
        entry_point = 'tasks.maze:Maze',
        kwargs = {'match_pairs': 1, 'max_steps': 3,
                  'high_level': True, 'task_name': 'Maze_L1'}
    )
    
    register(
        id = 'MA_L2',
        entry_point = 'tasks.maze:Maze',
        kwargs = {'match_pairs': 2, 'max_steps': 5,
                  'high_level': True, 'task_name': 'Maze_L2'}
    )
    
    register(
        id = 'MA_L3',
        entry_point = 'tasks.maze:Maze',
        kwargs = {'match_pairs': 3, 'max_steps': 7,
                  'high_level': True, 'task_name': 'Maze_L3'}
    )
    
    register(
        id = 'DE_L1',
        entry_point = 'tasks.decode:Decode',
        kwargs = {'related_num': 1, 'max_steps': 1, 
                  'high_level': True, 'task_name': 'Decode_L1'}
    )

    register(
        id = 'DE_L2',
        entry_point = 'tasks.decode:Decode',
        kwargs = {'related_num': 2, 'max_steps': 2, 
                  'high_level': True, 'task_name': 'Decode_L2'}
    )

    register(
        id = 'DE_L3',
        entry_point = 'tasks.decode:Decode',
        kwargs = {'related_num': 3, 'max_steps': 3, 
                  'high_level': True, 'task_name': 'Decode_L3'}
    )
    
    register(
        id = 'SE_L1',
        entry_point = 'tasks.selection:Selection',
        kwargs = {'mem_num': 1, 'max_steps': 2, 
                  'high_level': True, 'task_name': 'Selection_L1'}
    )

    register(
        id = 'SE_L2',
        entry_point = 'tasks.selection:Selection',
        kwargs = {'mem_num': 2, 'max_steps': 3,                   
                  'high_level': True, 'task_name': 'Selection_L2'}
    )

    register(
        id = 'SE_L3',
        entry_point = 'tasks.selection:Selection',
        kwargs = {'mem_num': 3, 'max_steps': 4,                   
                  'high_level': True, 'task_name': 'Selection_L3'}
    )

    register(
        id = 'MMA_L1',
        entry_point = 'tasks.memory_maze:Memory_Maze',
        kwargs = {'match_pairs': 1, 'max_steps': 4,
                  'high_level': True, 'task_name': 'Memory_Maze_L1'}
    )
    
    register(
        id = 'MMA_L2',
        entry_point = 'tasks.memory_maze:Memory_Maze',
        kwargs = {'match_pairs': 2, 'max_steps': 6,
                  'high_level': True, 'task_name': 'Memory_Maze_L2'}
    )
    
    register(
        id = 'MMA_L3',
        entry_point = 'tasks.memory_maze:Memory_Maze',
        kwargs = {'match_pairs': 3, 'max_steps': 8,
                  'high_level': True, 'task_name': 'Memory_Maze_L3'}
    )
 
    register(
        id = 'MFI_L1',
        entry_point = 'tasks.memory_filling:Memory_Filling',
        kwargs = {'match_pieces' : 1, 'max_steps': 2,
                  'high_level': True, 'task_name': 'Memory_Filling_L1'}
    )
    
    register(
        id = 'MFI_L2',
        entry_point = 'tasks.memory_filling:Memory_Filling',
        kwargs = {'match_pieces' : 2, 'max_steps': 3,
                  'high_level': True, 'task_name': 'Memory_Filling_L2'}
    )
    
    register(
        id = 'MFI_L3',
        entry_point = 'tasks.memory_filling:Memory_Filling',
        kwargs = {'match_pieces' : 3, 'max_steps': 4,
                  'high_level': True, 'task_name': 'Memory_Filling_L3'}
    )    

    register(
        id = 'MDE_L1',
        entry_point = 'tasks.memory_decode:Memory_Decode',
        kwargs = {'related_num': 1, 'max_steps': 2,
                  'high_level': True, 'task_name': 'Memory_Decode_L1'}
    )
    
    register(
        id = 'MDE_L2',
        entry_point = 'tasks.memory_decode:Memory_Decode',
        kwargs = {'related_num': 2, 'max_steps': 3,
                  'high_level': True, 'task_name': 'Memory_Decode_L2'}
    )
    
    register(
        id = 'MDE_L3',
        entry_point = 'tasks.memory_decode:Memory_Decode',
        kwargs = {'related_num': 3, 'max_steps': 4,
                  'high_level': True, 'task_name': 'Memory_Decode_L3'}
    )
    
REGISTER_TASKS()
