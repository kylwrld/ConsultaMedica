from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("api/signup/", views.Signup.as_view(), name='signup'),
    path("api/login/", views.Login.as_view(), name='login'),
    path("api/user/", views.User.as_view(), name='user'),
    path("api/queue/", views.FilaEndpoint.as_view(), name='fila'),
    path("api/consulta/user/", views.ConsultaUser.as_view(), name='consulta_user'),

    path("api/token/", views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh')
]
