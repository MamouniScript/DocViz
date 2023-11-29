from django.urls import path
from .views import upload_file, uploaded, display_visualization

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('uploaded/', uploaded, name='uploaded'),
    path('visualization/', display_visualization, name='display_visualization'),
]
