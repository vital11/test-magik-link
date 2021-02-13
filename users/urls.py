from django.urls import path
from users.views import HomeView, magic_signup, magic_login, activate

urlpatterns = [
        path('', HomeView.as_view(), name='home'),
        path('magic_signup/', magic_signup, name="magic_signup"),
        path('magic_login/', magic_login, name="magic_login"),
        path('activate/<uidb64>/<token>/', activate, name='activate'),
]
