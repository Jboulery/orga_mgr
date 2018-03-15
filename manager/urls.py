from django.urls import path

from . import views


app_name = 'manager'
urlpatterns = [
    #/
    path('', views.LoginFormView.as_view(), name='login'),
    #/register
    path('register', views.RegistrationFormView.as_view(), name='register'),
    #/<group_id>
    path('<int:group_id>/', views.group_index, name='group-index'),
    #/person/<person_id>
    path('person/<int:person_id>/', views.person_index, name='person-index'),
    #/person/add
    path('<int:group_id>/person/add/', views.person_create, name='person-create'),
    #/group/add
    path('group/add/', views.group_create, name='group-create'),
    #/group/delete
    path('group/delete/', views.group_delete, name='group-delete'),
    #/group/entity_move
    path('group/moveto', views.group_moveto, name='group-moveto'),
]