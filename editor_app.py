from flask import Flask, request, jsonify, send_from_directory, render_template, Response
import os
import base64
import time
from urllib.request import urlopen

app = Flask(__name__, static_folder='static', template_folder='.')

DATASET_PATH = 'circuit_dataset'
IMAGES_PATH = os.path.join(DATASET_PATH, 'images')
EDITED_PATH = os.path.join(DATASET_PATH, 'edited_images')

if not os.path.exists(EDITED_PATH):
    os.makedirs(EDITED_PATH)

@app.route('/')
def index():
    return render_template('editor.html')

@app.route('/api/images')
def list_images():
    if not os.path.exists(IMAGES_PATH):
        return jsonify([])
    # get all .png files
    images = [f for f in os.listdir(IMAGES_PATH) if f.endswith('.png')]
    # sort by modification time, newest first
    images.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGES_PATH, x)), reverse=True)
    return jsonify(images)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_PATH, filename)

@app.route('/edited/<path:filename>')
def serve_edited_image(filename):
    return send_from_directory(EDITED_PATH, filename)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        with urlopen(url) as response:
            data = response.read()
            return Response(data, mimetype=response.headers.get('content-type', 'image/png'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def save_edited():
    data = request.json
    filename = data.get('filename')
    image_data = data.get('image_data')

    if not filename or not image_data:
        return jsonify({'error': 'Missing filename or image data'}), 400

    # The image data is a base64 string: data:image/png;base64,iVBORw...
    if ',' in image_data:
        image_data = image_data.split(',')[1]

    try:
        binary_data = base64.b64decode(image_data)
        # Check if original filename is passed, we prepend 'edited_' and add a timestamp
        name, ext = os.path.splitext(filename)
        new_filename = f"edited_{name}_{int(time.time())}.png"
        filepath = os.path.join(EDITED_PATH, new_filename)
        
        with open(filepath, 'wb') as f:
            f.write(binary_data)
        
        return jsonify({
            'success': True,
             'message': 'Image saved successfully',
             'filename': new_filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run on port 5001 so it doesn't conflict with the main app
    app.run(debug=True, port=5001)
