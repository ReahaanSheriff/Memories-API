from django.urls import path,include
from . import views
from knox.views import LogoutView
from knox import views as knox_views


urlpatterns = [
    path('',views.memory),
    path('register/',views.register),
    path('login/',views.login),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
    path('changepassword/',views.changePassword),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('currentuser/',views.current_user),
]