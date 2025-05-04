from flask import Flask, jsonify, send_from_directory, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        result = subprocess.run(['python', 'script.py'], capture_output=True, text=True)
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/check-password', methods=['POST'])
def check_password():
    try:
        user_input = request.json.get('password', '')
        result = subprocess.run(['python', 'passdstrenth.py', user_input], capture_output=True, text=True)
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/list-files', methods=['GET'])
def list_files():
    try:
        files = os.listdir('.')
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/file-content', methods=['GET'])
def file_content():
    try:
        filename = request.args.get('filename')
        if not filename or not os.path.isfile(filename):
            return jsonify({'error': 'File not found'}), 404
        with open(filename, 'r') as file:
            content = file.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)