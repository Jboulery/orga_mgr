from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Organization, Group, Person


def group_index(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    ancestors = group.get_ancestors()
    descendants = group.get_children()
    persons = group.person_set.all()

    context = {
        'group': group,
        'ancestors': ancestors,
        'descendants': descendants,
        'persons': persons,
    }

    return render(request, 'manager/group.html', context)


def person_create(request, group_id):
    if request.method == 'GET':
        context = {'group_id': group_id}
        return render(request, 'manager/person_form.html', context)

    group = get_object_or_404(Group, pk=group_id)

