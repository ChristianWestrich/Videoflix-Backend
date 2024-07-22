from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True,
                                                read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'
