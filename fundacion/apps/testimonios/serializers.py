from rest_framework import serializers
from .models import Testimonio

class TestimonioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonio
        fields = '__all__'