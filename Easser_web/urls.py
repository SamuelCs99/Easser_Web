"""
URL configuration for Easser_web project.

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
from Easser_app.views import series, getUpdate, autocomplete_titulos, home, forEachEpisode, episode
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('series', series, name='series'),
    path('forEachEpisode', forEachEpisode, name='forEachEpisode'),
    path('episode/', episode, name='episode'),
    path('actualizar/', getUpdate, name='actualizar'),
    path('autocomplete/', autocomplete_titulos, name='autocomplete_titulos'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
