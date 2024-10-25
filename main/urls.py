from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('project/', views.project, name='project'),
    path('download/', views.download_file, name='download')
]
