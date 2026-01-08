from paolo_map.models import Marker
from paolo_map.serializers import (
    MarkerSerializer,
)
from django.test import TestCase,SimpleTestCase

class test_gis_serializer(TestCase):
    databases = '__all__'
    def test_serializer(self):

        Marker(size=1, location=[40.0,-111])
        print(MarkerSerializer('yaml', Marker))