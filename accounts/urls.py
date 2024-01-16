from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, ProfileView, activate
from book.views import ReturnView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('return/<int:pk>', ReturnView.as_view(), name='return_book'),
    
]
