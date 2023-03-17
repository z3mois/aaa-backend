from flask import Flask, request
from models.plate_reader import PlateReader
import logging
import io
from PIL import UnidentifiedImageError
import json


app = Flask(__name__)
plate_reader = PlateReader.load_from_file("./model_weights/plate_reader_model.pth")


@app.route('/')
def hello():
    return '<h1><center>Hello!</center></h1>'

@app.route('/readNumber', methods=["GET"])
def read_number():
    body = request.get_data()
    im = io.BytesIO(body)
    try:
        res = plate_reader.read_text(im)
    except UnidentifiedImageError:
        return {"error": 'invalid image'}, 400
    return {"name" : res}

@app.route('/images', methods=["GET", "POST"])
def read_image():
    data = json.loads(request.data)
    if "id" not in data:
        return {"error": ("invalid args", 400)}
    ids = data['id']
    return {"id" : ids}


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )
    app.config["JSON_AS_ASCII"] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
