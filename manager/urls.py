from django.urls import path

from . import views


app_name = 'manager'
urlpatterns = [
    #/manager/<group_id>
    path('<int:group_id>/', views.group_index, name='group-index'),
    #/manager/person/add
    path('<int:group_id>/person/add/', views.person_create, name='person-create'),
    #/manager/group/add
    path('group/add/', views.group_create, name='group-create'),
    #/manager/group/delete
    path('group/delete/', views.group_delete, name='group-delete'),
    #/manager/register
    path('register', views.UserFormView.as_view(), name='register'),
]