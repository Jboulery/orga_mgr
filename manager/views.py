from django.shortcuts import render, get_object_or_404

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