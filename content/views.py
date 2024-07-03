from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from django.core.cache.backends.base import DEFAULT_TIMEOUT


from Videoflix import settings
from content.models import Movie

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
class MovieSet(viewsets.ModelViewSet):
    queryset = Movie.object.all()