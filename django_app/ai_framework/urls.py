from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/agents/', include('agents.urls')),
    path('api/workflows/', include('workflows.urls')),
    path('api/monitoring/', include('monitoring.urls')),
]
