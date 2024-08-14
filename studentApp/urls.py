from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('', views.StudentView, name='student_list'),
    path('studentPost',views.StudentFormView,name = 'student_post'),
    path('create', views.StudentCreateView, name='student_create'),  # Admin view for creating details
    path('update/<int:pk>', views.StudentUpdateView, name='student_update'),  # Admin view for updating details
    path('/delete/<int:pk>', views.StudentDeleteView, name='student_delete'),  # Admin view for deleting details
   
    path('student/',views.StudentListView.as_view()),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('student/',views.CreateApiView.as_view()),
    path('student/',views.UpdateApiView.as_view()),
    path('student/',views.DeleteApiView.as_view()),
    
]