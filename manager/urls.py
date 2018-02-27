from django.urls import path

from . import views


app_name = 'manager'
urlpatterns = [
    #/<group_id>
    path('<int:group_id>/', views.group_index, name='group-index'),
    #/person/add
    path('<int:group_id>/person/add/', views.person_create, name='person-create'),
    #/group/add
    path('group/add/', views.group_create, name='group-create'),
    #/group/delete
    path('group/delete/', views.group_delete, name='group-delete'),
    #/register
    path('register', views.RegistrationFormView.as_view(), name='register'),
]