import numpy as np
import cv2 as cv
from flask import Flask, request, jsonify, send_file
import time



app = Flask(__name__)

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
