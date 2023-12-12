from time import sleep
import openai
import os


class OPENAIController:
    def __init__(self) -> None:
        self.client = openai.OpenAI(
            api_key="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"
        )

    def generateSuggestions(self, history):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=history
        )

        return response.choices[0].message.content

    def assistant_chat(self, history, new_message):
        print("In openai controller")
        print(history)
        sleep(10)
        history.append({"role": "user", "content": new_message})
        ai_answer = self.generateSuggestions(history)
        return ai_answer
