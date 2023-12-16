import os
import pyaudio
import wave
from playsound import playsound
import tempfile
from gtts import gTTS
from pathlib import Path
import librosa


latest_vaw = ""
latest_mp3 = ""


def record_voice():
    global latest_vaw
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    lang = "tr"

    temp_file_path = tempfile.mkstemp(suffix=".wav", dir="static")
    if os.path.exists(latest_vaw):
        os.remove(latest_vaw)
    latest_vaw = temp_file_path[1]

    p = pyaudio.PyAudio()

    print("Recording")
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Done!")

    wf = wave.open(temp_file_path[1], "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    return temp_file_path[1]


def tts(text, lang="en"):
    global latest_mp3
    temp_file_path = tempfile.mkstemp(suffix=".mp3", dir="static")
    if os.path.exists(latest_mp3):
        os.remove(latest_mp3)
    latest_mp3 = temp_file_path[1]

    mytext = text
    language = lang
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save(temp_file_path[1])
    duration = librosa.get_duration(path=temp_file_path[1])
    # return temp_file_path[1].split("/")[-1]
    return Path(temp_file_path[1]).stem + ".mp3", duration


def stt(openai_controller, save_location):
    return openai_controller.STT(save_location)
