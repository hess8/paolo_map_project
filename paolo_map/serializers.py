from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer,
)

from .models import Marker

class MarkerSerializer(
    GeoFeatureModelSerializer
):
    class Meta:
        fields = ("id", "size")
        geo_field = "location"
        model = Marker