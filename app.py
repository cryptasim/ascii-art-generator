from flask import Flask, request, render_template_string
from ascii_magic import AsciiArt
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASCII Art Generator</title>
</head>
<body>
    <h1>ASCII Art Generator</h1>
    <form id="uploadForm" enctype="multipart/form-data">
        <input type="file" name="image" id="image" accept="image/*" required>
        <button type="submit">Generate ASCII Art</button>
    </form>
    <div id="asciiArt">{{ ascii_art|safe }}</div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData();
            formData.append('image', document.getElementById('image').files[0]);

            const response = await fetch('/generate-ascii', {
                method: 'POST',
                body: formData
            });

            const result = await response.text();
            document.getElementById('asciiArt').innerHTML = result;
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, ascii_art="")

@app.route('/generate-ascii', methods=['POST'])
def generate_ascii():
    if 'image' not in request.files:
        return "No image file found", 400

    file = request.files['image']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    my_art = AsciiArt.from_image(file_path)
    ascii_html = my_art.to_html(columns=200, width_ratio=2)

    os.remove(file_path)  # Clean up the uploaded file

    return ascii_html

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
