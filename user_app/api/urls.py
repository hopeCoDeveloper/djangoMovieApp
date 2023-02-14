from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from user_app.api.views import registeration_view,logout_view
#from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    #token authentication
    path('login/',obtain_auth_token,name='login'),
    path('register/',registeration_view,name='register'),
    path('logout/',logout_view,name='logout'),
    #Jwt authentication
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]