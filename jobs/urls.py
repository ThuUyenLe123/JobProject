from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobsapp.urls')),
    path('', include('accounts.urls')),
    path('change/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change-password.html'), name='password_change'),
    path('change/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change-password-done.html'), name='password_change_done'),
]