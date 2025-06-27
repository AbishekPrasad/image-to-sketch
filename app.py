from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def pencil_sketch(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray_image
    blur = cv2.GaussianBlur(inverted, (251, 151), 0)
    invertedBlur = 255 - blur
    sketch = cv2.divide(gray_image, invertedBlur, scale=250.0)
    output_path = os.path.join('static', 'output.png')
    cv2.imwrite(output_path, sketch)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    output_path = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            output_path = pencil_sketch(path)
    return render_template('index.html', output_image=output_path)

if __name__ == '__main__':
    app.run(debug=True)
