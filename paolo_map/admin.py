from django.contrib.gis import admin
from .models import Marker
from leaflet.admin import LeafletGeoAdmin

# admin.site.register(Marker, admin.GISModelAdmin)
# admin.site.register(Marker, LeafletGeoAdmin)

class CustomGeoWidgetAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 6,
            'default_lon': -111.7208,
            'default_lat': 40.3433,
        },
    }

@admin.register(Marker)
class MarkerAdmin(CustomGeoWidgetAdmin):
    pass
