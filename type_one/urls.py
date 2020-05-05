from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('type_one.core.urls')),
    path('meal/', include('type_one.meal.urls')),
] 