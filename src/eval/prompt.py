import string

class Prompt():
    def __init__(self, task):
        self.task = task
        
    def generate_action_list(self, actions: list = None) -> str:
        """
        e.g. 
            actions: [action1, action2, action3]
            return: A) 'action1' B) 'action2' C) 'action3'
        """

        if actions is None:
            actions = self.task.actions
        options = ""
        for i, action in enumerate(actions):
            options += f"{string.ascii_uppercase[i]}) '{action}' "
        return options
    
    def generate_letter_list(self, actions: list = None) -> str:
        """
        e.g. 
            actions: [action1, action2, action3]
            return: A B C
        """

        if actions is None:
            actions = self.task.actions
        letters = ""
        for i in range(len(actions)):
            letters += f"{string.ascii_uppercase[i]}/"
        letters = letters[:-1]
        return letters
