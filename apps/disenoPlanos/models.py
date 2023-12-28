from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone

class Planos(models.Model):
    imagen = models.ImageField(upload_to='planos/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Imagen de plano: {self.imagen.name}' if self.imagen else 'Plano sin imagen'

    @staticmethod
    def convertir_imagen_a_bytes(imagen_path):
        try:
            extensiones_permitidas = ['.jpeg', '.jpg', '.png', '.webp']
            if not any(imagen_path.lower().endswith(ext) for ext in extensiones_permitidas):
                raise ValueError("Formato de imagen no admitido")

            with Image.open(imagen_path) as img:
                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                byte_sequence = buffer.getvalue()
                return byte_sequence
        except Exception as e:
            raise ValueError(f"Error al convertir la imagen a bytes: {e}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.imagen:
            byte_sequence = self.convertir_imagen_a_bytes(self.imagen.path)
            if byte_sequence:
                # Borra la imagen original antes de guardar la nueva
                self.imagen.delete(save=False)
                # Actualiza el campo imagen con la secuencia de bytes
                self.imagen.save('imagenes.jpg', ContentFile(byte_sequence), save=False)
                super().save(*args, **kwargs)
