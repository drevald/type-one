from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from type_one.records import views

urlpatterns = [
    path('',  views.records, name='default'),
    path('admin/', admin.site.urls),
    path('api/', include('type_one.api.urls')),    
    path('accounts/', include('type_one.core.urls')),
    path('records/', include('type_one.records.urls')),
    path('ingredients/', include('type_one.ingredients.urls')),
] 