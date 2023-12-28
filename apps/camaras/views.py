from django.shortcuts import render
from .models import Camara, Sensores

def camaras(request):
    # Obtener todas las cámaras desde la base de datos
    camaras = Camara.objects.all()

    # Obtener categorías únicas de la base de datos
    categorias_tipo = Camara.objects.values_list('tipo', flat=True).distinct()
    categorias_precio = Camara.objects.values_list('precio', flat=True).distinct()
    categorias_marca = Camara.objects.values_list('marca', flat=True).distinct()
    categorias_resolucion = Camara.objects.values_list('resolucion', flat=True).distinct()
    categorias_angulo_de_vision = Camara.objects.values_list('angulo_de_vision', flat=True).distinct()

    # Renderizar la página con la lista de cámaras y categorías
    return render(request, 'camaras.html', {
        'camaras': camaras,
        'categorias_tipo': categorias_tipo,
        'categorias_precio': categorias_precio,
        'categorias_marca': categorias_marca,
        'categorias_resolucion': categorias_resolucion,
        'angulo_de_vision': categorias_angulo_de_vision,
    })
