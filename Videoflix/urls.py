
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from Videoflix import settings
from users.views import LoginView, RegisterView, ActivateAccountView, ResetPasswordView, PasswordConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('auth/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_confirm/<uidb64>/<token>/', PasswordConfirmView.as_view(), name='password_confirm'),


]    + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
