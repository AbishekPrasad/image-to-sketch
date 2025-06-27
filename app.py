from flask import Flask, render_template, request, send_file
import cv2
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output_image = False
    if request.method == "POST":
        file = request.files["image"]
        if file:
            input_path = "static/input.jpg"
            output_path = "static/output.png"
            file.save(input_path)

            # Convert image to pencil sketch
            image = cv2.imread(input_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            inverted = 255 - gray
            blur = cv2.GaussianBlur(inverted, (251, 151), 0)
            inverted_blur = 255 - blur
            sketch = cv2.divide(gray, inverted_blur, scale=250.0)

            cv2.imwrite(output_path, sketch)
            output_image = True

    return render_template("index.html", output_image=output_image)

@app.route("/sketch")
def get_sketch():
    return send_file("static/output.png", mimetype='image/png')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render injects this variable
    app.run(debug=False, host="0.0.0.0", port=port)  # Required for external access
