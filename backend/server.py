# server.py (using Flask as an example)
from flask import Flask, request, jsonify
from sleep_detection import read_frame_and_annotatte
from flask_cors import CORS
from openai_controller import OPENAIController
from sound import tts, stt, record_voice

app = Flask(__name__)
CORS(app, origins="*")

openai_controller = OPENAIController()


@app.route("/process_image", methods=["GET"])
def process_image():
    processed_image_path, _ = read_frame_and_annotatte()
    return jsonify({"processed_image_path": processed_image_path})


@app.route("/chat", methods=["POST"])
def chat():
    history = request.json["history"]
    new_message = request.json["new_message"]
    resp = openai_controller.assistant_chat(history, new_message)
    return jsonify({"response": resp})


@app.route("/record", methods=["POST"])
def record():
    recorded_voice_file = record_voice()
    response = stt(openai_controller, recorded_voice_file)
    return jsonify({"response": response})


@app.route("/tts", methods=["POST"])
def tts_endpoint():
    message = request.json["message"]
    sound_file_path = tts(message)
    return jsonify({"sound_file_path": sound_file_path})


if __name__ == "__main__":
    app.run(debug=True)
