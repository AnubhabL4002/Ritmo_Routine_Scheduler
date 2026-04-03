from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # App pages
    path('', views.home_view, name='home'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('day/<str:day_key>/', views.day_view, name='day'),

    # API endpoints
    path('api/tasks/', views.api_tasks, name='api_tasks'),
    path('api/tasks/<str:task_id>/', views.api_task_delete, name='api_task_delete'),
    path('api/day/<str:day_key>/', views.api_day_data, name='api_day_data'),
    path('api/theme/', views.api_theme, name='api_theme'),
]
