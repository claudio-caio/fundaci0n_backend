from rest_framework.routers import DefaultRouter
from .views import TestimonioViewSet

router = DefaultRouter()
router.register(r'', TestimonioViewSet)

urlpatterns = router.urls