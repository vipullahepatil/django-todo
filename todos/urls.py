from django.urls import path
from . import views


app_name='todos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:todo_id>/delete', views.delete, name='delete'),
    path('update/<int:todo_id>/', views.update, name='update'),
    path('add/', views.add, name='add'),
]