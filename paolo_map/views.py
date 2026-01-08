from django.views.generic.base import TemplateView
from rest_framework import viewsets
from rest_framework_gis import filters

from .models import Marker
from .serializers import (
    MarkerSerializer,
)

class MarkersMapView(TemplateView):
    template_name = "index.html"

class MarkerViewSet(
    viewsets.ReadOnlyModelViewSet
):
    bbox_filter_field = "location"
    filter_backends = (
        filters.InBBoxFilter,
    )
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer
