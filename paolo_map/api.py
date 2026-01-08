from rest_framework import routers

from .viewsets import (
    MarkerViewSet,
)

router = routers.DefaultRouter()
router.register(
    # r"locations", MarkerViewSet,
    r"markers", MarkerViewSet
)

urlpatterns = router.urls
