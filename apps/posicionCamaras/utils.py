# En el archivo utils.py

def calcular_posiciones_optimas(medidas_habitacion, medidas_camara, angulo_vision, areas_interes):
    # Extraer las dimensiones de la habitación
    ancho_habitacion, largo_habitacion, alto_habitacion = medidas_habitacion

    # Extraer las dimensiones de la cámara
    ancho_camara, alto_camara = medidas_camara

    # Lista para almacenar las posiciones óptimas
    posiciones_optimas = []

    # Iterar sobre las áreas de interés y calcular posiciones óptimas
    for area_interes in areas_interes:
        x_area, y_area = area_interes

        # Lógica de cálculo para determinar la posición óptima
        # Esto es un ejemplo y debes adaptarlo según tus requisitos específicos
        x_camara_optima = x_area - ancho_camara / 2
        y_camara_optima = y_area - alto_camara / 2

        # Agregar la posición óptima a la lista
        posiciones_optimas.append((x_camara_optima, y_camara_optima))

    # Retorna la lista de posiciones óptimas
    return posiciones_optimas
