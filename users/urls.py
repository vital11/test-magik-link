from django.urls import path
from django.views.generic.base import TemplateView
from users.views import activate, signup, home

urlpatterns = [
        path('', home, name='home'),
        path('login', home, name='home'),
        path('signup/', signup, name="signup"),
        path('activate/<uidb64>/<token>/', activate, name='activate'),
]
