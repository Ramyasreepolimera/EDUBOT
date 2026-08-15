from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('courses/',views.courses, name='courses'),
    path('course_details/',views.courses_details, name='course-details'),
    path('contact/',views.contact,name='contact'),
]
