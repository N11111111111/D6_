from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from django.urls import path
from .views import upgrade_me, unsubscribe


urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('login/signup/',
         BaseRegisterView.as_view(template_name='signup.html'),
         name='signup'),

    path('upgrade/', upgrade_me, name='upgrade'),
    path('unsubscribe/', unsubscribe, name='unsubscribe')

]




