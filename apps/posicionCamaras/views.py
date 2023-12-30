# posicionCamaras/views.py
from django.shortcuts import render, redirect
from .models import Posicion
from django.http import JsonResponse
from apps.disenoPlanos.models import Planos
from apps.camaras.models import Camara
import cv2
import numpy as np
from sklearn.cluster import KMeans
from django.http import JsonResponse
import pytesseract
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random

def process_image_vertical(image_path):
    # Cargar la imagen en escala de grises
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Rotar la imagen 90 grados a la derecha
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # Aplicar umbralización
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    # Aplicar operaciones morfológicas para eliminar el ruido
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Configurar Tesseract para reconocer solo números 0-9 y las letras 'c' y 'm'
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789cm'
    text = pytesseract.image_to_string(img, config=custom_config)

    # Dividir el texto en líneas y filtrar las que contienen 'cm'
    measurements = [line for line in text.split('\n') if 'cm' in line]

    # Eliminar el 'cm' y convertir a entero
    measurements_numeros = [int(s.replace('cm', '')) for s in measurements]
    # Ordenar de mayor a menor
    measurements_ordenadas = sorted(measurements_numeros, reverse=True)
    # Convertir de nuevo a cadena con 'cm'
    measurements_final = [str(s) + 'cm' for s in measurements_ordenadas]

    return measurements_final

def process_image_horizontal(image_path):
    # Cargar la imagen en escala de grises
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Aplicar umbralización
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    # Aplicar operaciones morfológicas para eliminar el ruido
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Configurar Tesseract para reconocer solo números 0-9 y las letras 'c' y 'm'
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789cm'
    text = pytesseract.image_to_string(img, config=custom_config)
    text = text.replace('4', '1')

    # Dividir el texto en palabras y filtrar las que contienen 'cm'
    measurements = [word for word in text.split() if 'cm' in word]
    
    # Eliminar el 'cm' y convertir a entero
    measurements_numeros = [int(s.replace('cm', '')) for s in measurements]
    # Ordenar de mayor a menor
    measurements_ordenadas = sorted(measurements_numeros, reverse=True)
    # Convertir de nuevo a cadena con 'cm'
    measurements_final = [str(s) + 'cm' for s in measurements_ordenadas]

    return measurements_final

def get_measurements(request, id_plano):
    try: 
        # Obtener el plano por id
        plano = Planos.objects.get(id=id_plano)
        
        # Obtener la ruta de la imagen del plano
        plano_image = plano.imagen.path
        
        # Procesar la imagen para obtener las mediciones
        measurements_in_x = process_image_horizontal(plano_image)
        measurements_in_y = process_image_vertical(plano_image)
        measurements = {
            'Medidas en Y': measurements_in_y,
            'Medidas en X': measurements_in_x
        }
        
        return {"measurements": measurements}
    except Planos.DoesNotExist:
        # Manejar el caso cuando el plano no se encuentra
        return JsonResponse({"error": "Plano no encontrado"})

def get_camera_coverage(camera):
    return np.pi * (camera.alcance_cm ** 2)

def calculate_random_position(width, height):
    # Elegir un lado aleatorio: 0 = arriba, 1 = derecha, 2 = abajo, 3 = izquierda
    side = random.randint(0, 3)

    if side == 0:  # Arriba
        return np.array([[random.uniform(4, width-4), height-4]])
    elif side == 1:  # Derecha
        return np.array([[width-4, random.uniform(4, height-4)]])
    elif side == 2:  # Abajo
        return np.array([[random.uniform(4, width-4), 4]])
    else:  # Izquierda
        return np.array([[4, random.uniform(4, height-4)]])

def calculate_best_corner_position(width, height):
    # Las mejores posiciones después del centro serían las esquinas
    return calculate_random_position(width, height)

def posicion_camaras(request, id_plano, id_camara):
    try:
        measurements_dict = get_measurements(request, id_plano)
        measurements = measurements_dict['measurements']
        width_str = measurements['Medidas en X'][0]
        height_str = measurements['Medidas en Y'][0]

        # Extraer los números y convertirlos a enteros
        width = int(width_str.split('cm')[0])
        height = int(height_str.split('cm')[0])

        camera = Camara.objects.get(id=id_camara)
        camera_coverage = get_camera_coverage(camera)

        area = width * height
        num_cameras = np.floor(area / camera_coverage).astype(int)

        if num_cameras >= 1:
            camera_positions = calculate_best_corner_position(width, height)
        else:
            camera_positions = []

        # Convertir camera_positions a una lista de Python y luego a un diccionario
        camera_positions_list = camera_positions.tolist()
        camera_positions_dict = {'camera_positions': camera_positions_list, 'house': {'width': width, 'height': height}}

        return camera_positions_dict
    except IndexError:
        return redirect('disenoPlanos')


def generar_plano(request, id_plano, id_camara): 
    try:
        measurements_camara_house = posicion_camaras(request, id_plano, id_camara)
        fig, ax = plt.subplots()
        ax.add_patch(plt.Rectangle((0,0), measurements_camara_house['house']['width'], measurements_camara_house['house']['height'], fill=None, edgecolor='black'))
        
        camera_positions = measurements_camara_house['camera_positions']
        for position in camera_positions:
            if position[0] == 0 and position[1] == 0:  # Si la posición es una esquina
                ax.plot(position[0], position[1], 'ro', markersize=15)  # Aumenta el tamaño en un 25%
            else:
                ax.plot(position[0], position[1], 'ro')
        
        ax.set_xlim([0, measurements_camara_house['house']['width']])
        ax.set_ylim([0, measurements_camara_house['house']['height']])
        
        # Establecer las marcas en los ejes x e y para que estén separadas por 10 unidades
        ax.set_xticks(np.arange(0, measurements_camara_house['house']['width'], 20))
        ax.set_yticks(np.arange(0, measurements_camara_house['house']['height'], 20))
        
        plt.savefig('static/images/plano_with_cameras.png')
        
        return render(request, 'prueba.html', {
            'image_path': 'images/plano_with_cameras.png',
        })
    except KeyError:
        print('Intenta con una foto menos borrosa')
        return redirect('disenoPlanos')

def calcular_posicion_optima(ancho_casa, alto_casa):
    
    return calcular_posicion_optima_existente(ancho_casa, alto_casa)

def calcular_posicion_optima_existente(ancho_casa, alto_casa):
    # ... lógica para calcular la posición óptima ...

    return {'x': 100, 'y': 150}  # Por ahora, devuelve una posición de ejemplo
