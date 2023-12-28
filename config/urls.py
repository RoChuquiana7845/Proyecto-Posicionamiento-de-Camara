"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from apps.posicionCamaras.views import
from apps.disenoPlanos.views import disenoPlanos
from apps.Home.views import inicio
from apps.camaras.views import camaras
from apps.posicionCamaras.views import generar_plano
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('camaras/', camaras, name='camaras'),
    path('disenoPlanos/', disenoPlanos, name='disenoPlanos'),
    path('posicionCamaras/<int:id_plano>/<int:id_camara>/calcular', generar_plano, name='posicionCamaras'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)