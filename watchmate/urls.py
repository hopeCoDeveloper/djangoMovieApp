from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include('watchlist_app.api.urls')),
    path('account/',include('user_app.api.urls')),
    #temporary login url
    # path('api-auth/',include('rest_framework.urls'))
    path('api/schema/', SpectacularAPIView.as_view() , name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
