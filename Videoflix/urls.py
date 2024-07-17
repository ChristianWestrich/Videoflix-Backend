
from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from users.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('auth/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('pw_reset/', PasswordResetView.as_view(), name='pw_reset'),
    path('pw_confirm', PasswordResetConfirmView.as_view(), name='pw_confirm'),


]    + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
