from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Planos

@admin.register(Planos)
class PlanosAdmin(admin.ModelAdmin):
    list_display = ( 'mostrar_imagen',)

    def mostrar_imagen(self, obj):
        # Función para mostrar la imagen en el panel de administración
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.imagen.url)
        else:
            return 'No hay imagen'

    mostrar_imagen.short_description = 'Imagen del plano'