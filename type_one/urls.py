from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from type_one.records import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',  views.records, name='default'),
    path('admin/', admin.site.urls),
    path('accounts/', include('type_one.core.urls')),
    path('records/', include('type_one.records.urls')),
    path('ingredients/', include('type_one.ingredients.urls')),
] 