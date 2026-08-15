from django.urls import path
from . import views

urlpatterns = [
   
    path('stu-login/', views.stu_login, name='stu-login'),
    path('register/',views.stu_register, name='register'),
    path('stu_dashboard/',views.stu_dashboard,name='stu-dashboard'),
    path('edubot/',views.edubot,name='edubot'),
    path('about/',views.about,name='about'),
    path('material/',views.materials,name="materials"),
    path('profile/',views.profile, name='profile'),
    path('feedback/<int:id>/',views.stu_feedback,name='feedback'),
    path('stu-logout/',views.stu_logout,name='logout'),
    
]
