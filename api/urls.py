from django.urls import path
from . import views

urlpatterns = [
    path('summary/',views.userQuizSummaryView,name='user_quiz_summary_view'),
    path('detail/',views.userQuizDetailView,name='user_quiz_detail_view'),
    path('create_summary/',views.createUserQuizView,name='create_summary'),
    path('create_detail/',views.createUserDetailView,name='create_detail'),
    path('update_detail/<int:pk>/',views.updateUserDetailView,name='update_detail'),
    path('update_summary/<int:pk>/',views.updateUserSummaryView,name='update_summary'),
    path('collaborate/',views.collaborateView,name='user_collaborate_view'),
]
