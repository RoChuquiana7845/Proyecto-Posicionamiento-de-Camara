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

            return redirect('posicionCamaras', id_plano=plano.id, id_camara=2 )

        else:
            messages.error(request, 'Hubo un error al cargar el plano. Verifica los datos ingresados.')

    else:
        form = PlanosForm()
    return render(request, 'disenoPlanos.html', {'form': form, 'anguloVision': anguloVision})


