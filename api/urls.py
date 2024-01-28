from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("api/teste/", views.teste, name='teste'),
    path("api/signup/", views.Signup.as_view(), name='signup'),
    # path("api/signup2/", views.signup, name='signup'),

    path("api/token/", views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh')
]
