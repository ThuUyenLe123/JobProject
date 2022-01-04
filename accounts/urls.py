from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from jobsapp.views.employee import profile_employee
from .views import *

app_name = "accounts"

urlpatterns = [
    path('employee/register', register_employee, name='employee-register'),
    path('employer/register', register_employer, name='employer-register'),
    path('employee/profile/update', profile_employee, name='employee-profile-update'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
] 

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
