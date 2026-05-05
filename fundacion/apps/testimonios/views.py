from rest_framework import viewsets
from .models import Testimonio
from .serializers import TestimonioSerializer

class TestimonioViewSet(viewsets.ModelViewSet):
    queryset = Testimonio.objects.all().order_by('-fecha_creacion')
    serializer_class = TestimonioSerializer