
from django.urls import path
from .views import upload, latest_image, classify_image

urlpatterns = [
    path('upload/', upload, name='upload'),
    path('latest_image/', latest_image, name='latest_image'),
    path('classify_image/', classify_image, name='classify_image'),
]