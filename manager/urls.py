from django.urls import path

from . import views


app_name = 'manager'
urlpatterns = [
    #/manager/<group_id>
    path('<int:group_id>/', views.group_index, name='group-index'),
    #/manager/person/add
    path('<int:group_id>/person/add/', views.person_create, name='person-create')
]