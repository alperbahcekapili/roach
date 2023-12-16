import openai

client = openai.OpenAI(api_key="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")


class OPENAI_STT:
    def __init__(self) -> None:
        pass

    def STT(save_location):
        audio_file = open(save_location, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
        return transcript.text
