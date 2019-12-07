from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'goal_app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    path('goals', views.AllGoalsView.as_view(), name='goals'),
    path('goals/create/', views.goal_create, name='goal_create'),
    path('goals/update/<int:pk>', views.goal_update, name='goal_update'),
    path('goals/delete/<int:pk>', views.goal_delete, name='goal_delete'),
    path('goals/subgoals/delete/<int:pk>', views.subgoal_delete, name='subgoal_delete'),
    path('goals/activity/delete/<int:pk>', views.activity_delete, name='activity_delete'),
    path('goals/<int:pk>/subgoals/edit/', views.GoalsSubgoalsUpdateView.as_view(), name='goals_subgoals_update'),
    path('goals/progress', views.check_activity, name='check_activity')
]
