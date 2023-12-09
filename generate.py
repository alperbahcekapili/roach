import openai
import os

client = openai.OpenAI()


class OPENAIController:
    def __init__(self) -> None:
        pass
    def generateSuggestions(self, text):
     
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=text
        )
        

        return response.choices[0].message