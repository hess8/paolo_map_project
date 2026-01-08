"""
URL configuration for paolo_map project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import include, path
from paolo_map.views import MarkersMapView
urlpatterns = [
    # path('', views.index, name='index'),
    path("map/", TemplateView.as_view(template_name="map.html"),),
    # path("map/", MarkersMapView.as_view()
    # ),
    path(
        "api/", include("paolo_map.api")
    ),
    path('admin/', admin.site.urls)
    #don't put in path for "markers"...the tutorial uses 2 apps, not one.
]
