from flask import Flask, request, jsonify
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
        print('save to image.jpg')
        image.save('image.jpg')

        return jsonify({'image_size': image_size, 'image_name': image_name, 'image_width': width, 'image_height': height})
    else:
        return jsonify({'Name': 'No image provided'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)