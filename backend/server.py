# server.py (using Flask as an example)
from flask import Flask, jsonify
from sleep_detection import read_frame_and_annotatte
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")


@app.route("/process_image", methods=["GET"])
def process_image():
    processed_image_path, _ = read_frame_and_annotatte()
    return jsonify({"processed_image_path": processed_image_path})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
