from django.shortcuts import render, redirect
from .forms import PlanosForm
from django.contrib import messages
import cv2
import pytesseract
from django.urls import reverse


def disenoPlanos(request):
    # Obtén el valor de anguloVision (puede ser de la solicitud GET o POST)
    anguloVision = request.GET.get('anguloVision', None)
    if request.method == 'POST':
        form = PlanosForm(request.POST, request.FILES)
        if form.is_valid():
            plano = form.save(commit=False)

            plano.save()

            # Configura la ruta al ejecutable de Tesseract OCR
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

            # Cargamos la imagen
            original = cv2.imread(plano.imagen.path)

            # Reconoce números y comas
            texto_numeros_comas = pytesseract.image_to_string(original,
                                                              config='--psm 6 -c tessedit_char_whitelist=0123456789,')
            texto_numeros_comas = texto_numeros_comas.replace(',', '.')

            # Almacena los textos reconocidos en una lista
            textos_reconocidos = [texto_numeros_comas]

            # Almacena los textos reconocidos en una tupla
            medidas = tuple(texto_numeros_comas.split())

            print(medidas)

            # Utiliza reverse para obtener la URL con los argumentos de palabra clave
            url = reverse('posicionCamaras')

            # Agrega los argumentos de palabra clave a la URL
            url += f'?anguloVision={anguloVision}'

            return redirect(url)

        else:
            messages.error(request, 'Hubo un error al cargar el plano. Verifica los datos ingresados.')

    else:
        form = PlanosForm()
    return render(request, 'disenoPlanos.html', {'form': form, 'anguloVision': anguloVision})


