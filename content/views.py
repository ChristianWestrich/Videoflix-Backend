from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from django.core.cache.backends.base import DEFAULT_TIMEOUT


from Videoflix import settings
from content.models import Movie
from content.serializer import MovieSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    