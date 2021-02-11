from django.urls import path
from django.views.generic.base import TemplateView
from users.views import activate, signup, home, magic_send, magic_activate

urlpatterns = [
        path('', home, name='home'),
        path('signup/', signup, name="signup"),
        path('activate/<uidb64>/<token>/', activate, name='activate'),
        path('magic_send/', magic_send, name="magic_send"),
        path('magic_activate/<uidb64>/<token>/', magic_activate, name='magic_activate'),
]
