from . import views
from todoapp.api import resources
from django.urls import path
from django.conf.urls import include, url
app_name = 'todoapp'

urlpatterns = [
    path('', views.my_goals, name='my-goals'),
    path('projects/show/<int:goal_id>/', views.show_projects_for_goal, name='show_projects_for_goal'),
    path('tasks/edit_task/<int:project_id>/', views.edit_task, name='add_new_task'),
    path('tasks/edit_task/<int:project_id>/<int:task_id>/', views.edit_task, name='edit_task'),
    path('projects/edit_project/<int:goal_id>/',views.edit_project, name='add_new_project'),
    path('projects/edit_project/<int:goal_id>/<int:project_id>',views.edit_project, name='edit_project'),
    path('today/', views.show_todays_tasks, name='show_todays_tasks'),


    # path('tasks/edit/<int:task_id>', views.edit_task, name='edit_task'),
    url(r'^api/manage_task/$', resources.manage_task, name='manage-task'),
    url(r'^api/manage_project/$', resources.manage_project, name='manage-project')
]
