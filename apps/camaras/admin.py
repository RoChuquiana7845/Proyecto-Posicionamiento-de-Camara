from django.contrib import admin

# Register your models here.

from .models import Camara
from .models import Sensores

@admin.register(Camara)
class CameraAdmin(admin.ModelAdmin):
    # Puedes personalizar la visualización de los registros de tu modelo en el panel de administración
    list_display = ('nombre','tipo', 'angulo_de_vision', 'precio', 'marca')


@admin.register(Sensores)
class SensoresAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'precio', 'marca')

