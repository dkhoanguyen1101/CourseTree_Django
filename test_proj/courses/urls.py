from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('viewProfile/<int:User_id>/', views.viewProfile, name='viewProfile'),
    path('viewCourse/<int:Course_id>/', views.viewCourse, name='viewCourse'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ajax/load_num/', views.load_num, name='ajax_load_num'),
    path('delete/<Course_id>/', views.delete_course, name='delete_course'),
    path('changeCourse/<int:node_id>', views.changeCourse, name='changeCourse'),
    path("addChild/<int:node_id>", views.addChild, name='addChild'),
    path("deleteNode/<int:node_id>", views.deleteNode, name='deleteNode'),
    path("logout/", views.logout_view, name='deleteNode'),
    path('signup/', views.signup, name='signup'),




]
