from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('profile/<int:Person_id>/', views.profile, name='profile'),
    path('viewCourse/<int:Course_id>/', views.viewCourse, name='viewCourse')
]
