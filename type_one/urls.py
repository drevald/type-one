from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('', include('type_one.records.urls')),
    path('admin/', admin.site.urls),
    path('records/', include('type_one.records.urls')),
    path('ingredients/', include('type_one.ingredients.urls')),
] 