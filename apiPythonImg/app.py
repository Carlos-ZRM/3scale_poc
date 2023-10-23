import os
import psutil
import time
import numpy as np
import cv2 as cv
from flask import Flask, request, jsonify, send_file, render_template
from flask_socketio import SocketIO
import time



app = Flask(__name__)
socketio = SocketIO(app)

concurrent_connections = 0


@app.route('/', methods=['GET', 'POST'])
def print_headers():
    headers = dict(request.headers)
    return headers

@socketio.on('connect')
def handle_connect():
    global concurrent_connections
    concurrent_connections += 1
    print(f"Client connected. Concurrent Connections: {concurrent_connections}")
    socketio.emit('connection_update', concurrent_connections, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global concurrent_connections
    concurrent_connections -= 1
    print(f"Client disconnected. Concurrent Connections: {concurrent_connections}")
    socketio.emit('connection_update', concurrent_connections, broadcast=True)

@app.route('/socket')
def index():
    return render_template('index.html')


def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory_info.percent,
    }

# Function to calculate uptime
def get_uptime():
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time
    return uptime

# Health check route
@app.route('/health')
def health_check():
    process_info = get_system_info()
    uptime = get_uptime()
    response_time = time.time()
    
    return jsonify({
        "process_info": process_info,
        "uptime_seconds": uptime,
        "response_time": response_time
    })

def keypoints(img_src):
    img = cv.imread(img_src)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    sift = cv.SIFT_create()
    kp = sift.detect(gray, None)
    img_with_keypoints = cv.drawKeypoints(gray, kp, img)
    timestamp = int(time.time())
    # Guarda la imagen con puntos clave dibujados
    output_path = 'img/' + img_src +str(timestamp) +'_keypoints.jpg'
    cv.imwrite(output_path, img_with_keypoints)

    return output_path

@app.route('/procesar-imagen', methods=['POST'])
def procesar_imagen():
    try:
        if 'imagen' not in request.files:
            return jsonify({'error': 'No se proporcionó una imagen'}), 400

        imagen = request.files['imagen']
        imagen.save('input_image.jpg')

        output_image_path = keypoints('input_image.jpg')

        return send_file(output_image_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
