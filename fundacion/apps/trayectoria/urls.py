from rest_framework.routers import DefaultRouter

from .views import CasoExitoViewSet

router = DefaultRouter()
router.register(r'casos', CasoExitoViewSet)

urlpatterns = router.urls
