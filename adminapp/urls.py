from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/',views.admin_login, name='admin-login'),
    path('admin-dashboard/',views.admin_dashboard,name='admin-dashboard'),
    path('pending-students/',views.pending_students,name='pending-Students'),
    path('accept/<int:id>/',views.accept_stu,name='accept_stu'),
    path('reject_stu/<int:id>/',views.reject_stu,name='reject_stu'),
    path('all-students/',views.all_students,name='all-Students'),
    path('delete_stu/<int:id>/',views.delete_stu,name='delete_stu'),
    path('add-materials/',views.add_materials,name='add-study-material'),
    path('manage-materials/',views.manage_study_material,name='manage-study-material'),
    path('edit_materials/<int:id>/',views.edit_material,name='edit_material'),
    path('delete/<int:id>/',views.delete_material,name='delete_material'),
    path('sentiment/',views.sentiment_analysis,name='sentiment'),
    path('graph/',views.sentiment_graph, name='graph'),
    path('logout/',views.admin_logout,name='admin-logout'),
]
