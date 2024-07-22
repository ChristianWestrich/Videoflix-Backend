from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from Videoflix import settings
from content.models import Movie
from content.serializer import MovieSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



class MovieViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)