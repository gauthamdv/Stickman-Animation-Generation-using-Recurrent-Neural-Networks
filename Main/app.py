import generate_animations as g

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Save the file to the upload folder
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully!", "filePath": file_path})

@app.route('/api/generate-animation', methods=['POST'])
def generate_animation():
    try:
        g.main()# Launch the Windows function in a separate Python process

        return jsonify({"success": True, "output": "Animation Generated Successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/show-animation', methods=['POST'])
def show_animation():
    try:
        import preview as p
        p.show()            
        
        return jsonify({"success": True, "output": "Window Closed."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=False)