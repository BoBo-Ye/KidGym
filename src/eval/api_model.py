import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

class APIModel():
    def __init__(self, model_name: str):
        self.name = model_name
        self.client = OpenAI(base_url = os.getenv("OPENAI_API_BASE"), api_key = os.getenv("OPENAI_API_KEY"))
        self.reset()
        
    def set_system_prompt(self, system_prompt: str):
        """
        Set the system prompt for the model.
        
        Args:
            system_prompt (str): The system prompt to set.
        """
        
        self.system_prompt = system_prompt
        self.history = [{
            "role": "system",
            "content": [
                {
                    "type": "text", 
                    "text": self.system_prompt
                }
            ]
        }]
        
    def reset(self):
        """
        Reset the model history.
        """
        self.history = []
        self.img_num = 0
    
    def handle_message(self, prompt_input: str = None, img_input: str | list = None, is_user: bool = True) -> dict:
        """
        Handle the message in the standard format.
        
        Args:
            prompt_input (str): The text prompt.
            image_input (str | list): The image path or list of image paths.
            is_user (bool): Whether the message is from the user or the assistant.
            
        Format:
            messages=[
                {
                    "role": "user",
                    "content": [
                        {   
                            "type": "text", 
                            "text": "What is the difference between these two images?"
                        },
                        {
                            "type": "image_url",
                            "image_url": 
                            {
                                "url": f"data:image/jpeg;base64,{base64_image1}"
                            }
                        },
                        {
                            "type": "image_url",
                            "image_url": 
                            {
                                "url": f"data:image/jpeg;base64,{base64_image2}"
                            }
                        }
                    ]
                }
            ]
        """

        if type(img_input) == str:
            img_input = [img_input]
            
        if img_input:
            assert is_user, "Image input only support user message."
            for img_path in img_input:
                base64_image = encode_image(img_path)
                self.history.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": f"<Image {self.img_num + 1}>: "
                        },
                        {
                            "type": "image_url",
                            "image_url": 
                            {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                })
                self.img_num += 1
        
        if prompt_input:
            message = {
                "role": "user" if is_user else "assistant",
                "content": [
                    {
                        "type": "text", 
                        "text": prompt_input
                    }
                ],
            }
        
            self.history.append(message)
            
        return self.history
    
    def chat(self, prompt_input, img_input = None):
        """
        Chat with the model.
        """
        conversation = self.handle_message(prompt_input, img_input, is_user = True)
        response = self.client.chat.completions.create(
            model = self.name,
            messages = conversation
        ).choices[0].message.content
        
        self.handle_message(response, is_user = False)
        return response

if __name__ == "__main__":
    model = APIModel("gpt-5")
    model.set_system_prompt("You are a helpful assistant.")
    response = model.chat("Hello!")
    print(response)