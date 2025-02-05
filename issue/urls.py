from django.urls import path
from . import views

urlpatterns = [
    path('issue-details/<int:pk>/', views.issue_details, name='issue-details'),
    path('create-issue/', views.create_issue, name='create-issue'),
    path('update-issue/<int:pk>/', views.update_issue, name='update-issue'),
    path('all-issues/', views.all_issues, name='all-issues'),
    path('issue-queue/', views.issue_queue, name='issue-queue'),
    path('accept-issue/<int:pk>/', views.accept_issue, name='accept-issue'),
    path('close-issue/<int:pk>/', views.close_issue, name='close-issue'),
    path('workspace/', views.workspace, name='workspace'),
    path('all-issues-resolved/', views.all_issues_resolved, name='all-issues-resolved'),
    path('real-time-issue-data/', views.real_time_issue_data, name='real_time_issue_data'),
]
