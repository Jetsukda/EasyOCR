import json

import cv2
import numpy as np
from pytictoc import TicToc

from easyocr import Reader
from flask import Flask, request

timer = TicToc()
reader = Reader(["th", "en"])


app = Flask(__name__)


@app.route("/detect", methods=["POST"])
def detect():
    file = request.files['image']
    contents = file.read()
    img = np.array(bytearray(contents), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    horizontal, free = reader.detect(img)
    horizontal = np.array(horizontal, dtype=np.int32).tolist()
    quad = np.array(free, dtype=np.int32).tolist()
    return json.loads(json.dumps({'msg': 'success', "hor": horizontal, "quad": quad}))


@app.route("/recognize", methods=["POST"])
def recognize():
    file = request.files['image']
    horizontal = request.args.getlist(key="horizontal", type=list)
    quad = request.args.getlist(key="quad", type=list)

    horizontal = np.array(horizontal)
    quad = np.array(quad)
    contents = file.read()
    img = np.array(bytearray(contents), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    result = reader.recognize(img, horizontal, quad)
    return json.loads(json.dumps({'msg': 'success', "results": horizontal}))


@app.route("/readtext", methods=["POST"])
def readtext():
    file = request.files['image']
    contents = file.read()
    img = np.array(bytearray(contents), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    results = reader.readtext(img)
    output = []
    for loc, text, prob in results:
        data = {"text": text, "loc": loc, "prob": prob}
        output.append(data)
    return json.loads(json.dumps({'msg': 'success', "results": str(output)}))


if __name__ == "__main__":
    app.run(debug=True, host=18, port=8666)
