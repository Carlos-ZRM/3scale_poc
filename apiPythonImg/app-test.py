import os
import psutil
import time
import ctypes
import numpy as np

from flask import Flask, request, jsonify, send_file, render_template
from flask_socketio import SocketIO
import time



app = Flask(__name__)
socketio = SocketIO(app)

concurrent_connections = 0
MEMORY_SLEEP = int(os.environ.get('MEMORY_SLEEP', 5 ))
MEMORY_SIZE_MB = int(os.environ.get('MEMORY_SIZE_MB', 10 ))


@app.route('/', methods=['GET', 'POST'])
def print_headers():
    headers = dict(request.headers)
    return headers

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


def allocate_memory(mb):
    # Reserva memoria en bloques de 1 MB
    size_in_bytes = mb * 1024 * 1024
    arr = bytearray(size_in_bytes)
    return arr

def release_memory(arr):
    # Libera la memoria reservada
    ctypes.c_void_p.from_buffer(arr)

@app.route('/memory', methods=['GET'])
def test_endpoint():
    try:
        # Reserva 50 MB de memoria
        allocated_memory = allocate_memory(MEMORY_SIZE_MB)

        # Espera 5 segundos
        time.sleep(MEMORY_SLEEP)

        # Libera la memoria después de 5 segundos
        release_memory(allocated_memory)

        return "Prueba de rendimiento exitosa."
    except Exception as e:
        return f"Error durante la prueba: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
