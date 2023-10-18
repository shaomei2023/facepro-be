from flask import Flask, request, jsonify
from face_nn.retinaface import Retinaface
from PIL import Image
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        image_data = image.read()
        image_size = len(image_data)
        image_name = image.filename

        # 处理图像并返回大小和名称
        # 例如，您可以使用 Pillow 来获取图像尺寸
        image = Image.open(io.BytesIO(image_data))
        width, height = image.size

        image = image.rotate(270, expand=True)  # .resize(image.size)
        retinaface = Retinaface()
        result = retinaface.recognize_faces(image)
        print(result)
        if type(result) != list:
            return jsonify({'result': 'No face detected!'})
        # print(result[0])

        # return jsonify({'image_size': image_size, 'image_name': image_name, 'image_width': width, 'image_height': height})
        return jsonify(result[0])
    else:
        return jsonify({'result': 'No image provided'})

@app.route('/test_post', methods=['POST'])
def test_post():
    result = {'name': 'obama', 'distance': '0.9894'}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)