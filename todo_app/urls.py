from django.urls import path
from . import views

#url mapping
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('todo-create/', views.ToDoCreateView.as_view(), name='create_todo'),
    path('todo-list/', views.TodoListView.as_view(), name='todo_list'),
    path('todo-update/<int:pk>/', views.TodoUpdateView.as_view(), name='todo_update'),
    path('todo-delete/<int:pk>/', views.TodoDeleteView.as_view(), name='todo_delete'),
]