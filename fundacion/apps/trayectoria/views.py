from rest_framework import viewsets
from .models import CasoExito
from .serializers import CasoExitoSerializer

class CasoExitoViewSet(viewsets.ModelViewSet):
    queryset = CasoExito.objects.prefetch_related('galeria').all()
    serializer_class = CasoExitoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sector = self.request.query_params.get('sector')
        if sector:
            queryset = queryset.filter(sector=sector)
        return queryset
