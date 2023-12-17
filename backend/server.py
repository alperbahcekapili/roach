# server.py (using Flask as an example)
from flask import Flask, request, jsonify
from sleep_detection import read_frame_and_annotatte
from flask_cors import CORS
from openai_controller import OPENAIController
from Models.function_matching import FunctionMatcher
from sound import tts, stt, record_voice
import time


__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")


app = Flask(__name__)
CORS(app)

openai_controller = OPENAIController()
function_matcher = FunctionMatcher()
print(function_matcher.get_similar("Exit"))


@app.route("/process_image", methods=["GET"])
def process_image():
    processed_image_path, is_sleeping = read_frame_and_annotatte()
    return jsonify(
        {"processed_image_path": processed_image_path, "is_sleeping": is_sleeping}
    )


@app.route("/chat", methods=["POST"])
def chat():
    print(request.json)
    history = request.json["history"]
    resp = openai_controller.assistant_chat(history)
    return jsonify({"response": resp})


@app.route("/record", methods=["POST"])
def record():
    recorded_voice_file = record_voice()
    time.sleep(6)
    response = stt(openai_controller, recorded_voice_file)
    return jsonify({"response": response})


@app.route("/tts", methods=["POST"])
def tts_endpoint():
    message = request.json["response"]
    sound_file_path, duration = tts(message)
    return jsonify({"sound_file_path": sound_file_path, "duration": duration})


if __name__ == "__main__":
    app.run(debug=False)
