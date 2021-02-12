from django.urls import path
from users.views import home, activate, signup, login_existing_user, activate_existing_user

urlpatterns = [
        path('', home, name='home'),
        path('signup/', signup, name="signup"),
        path('activate/<uidb64>/<token>/', activate, name='activate'),
        path('login_existing_user/', login_existing_user, name="login_existing_user"),
        path('activate_existing_user/<uidb64>/<token>/', activate_existing_user, name='activate_existing_user'),
]
