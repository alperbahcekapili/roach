from time import sleep
import openai
import os
import ast


class OPENAIController:
    def __init__(self) -> None:
        self.client = openai.OpenAI(
            api_key="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"
        )

    def generateSuggestions(self, history):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=list(history)
        )

        return response.choices[0].message.content

    def assistant_chat(self, history):
        ai_answer = self.generateSuggestions(history)
        return ai_answer

    def STT(self, save_location):
        audio_file = open(save_location, "rb")
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
        return transcript.text
