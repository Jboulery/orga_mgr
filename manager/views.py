from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction

from .forms import UserForm
from .models import Organization, Group, Person
from django.contrib.auth.models import User


def get_group_tree(group_id):
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

    return context


def group_index(request, group_id):
    context = get_group_tree(group_id)
    return render(request, 'manager/group.html', context)


def person_create(request, group_id):
    if request.method == 'GET':
        context = {'group_id': group_id}
        return render(request, 'manager/person_form.html', context)

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        date_of_birth = request.POST['date_of_birth']
        address = request.POST['address']
        try:
            request.POST['is_manager']
            is_manager = True
        except:
            is_manager = False
        try:
            request.POST['is_admin']
            is_admin = True
        except:
            is_admin = False
        group_id_input = int(request.POST['group_id'])

        group = Group.objects.get(pk=group_id_input)

        username = (firstname[0].lower() + lastname).lower()
        password = User.objects.make_random_password()

        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
            person = Person.objects.create(user=user, group=group, is_manager=is_manager, is_admin=is_admin, gender=gender, date_of_birth=date_of_birth, address=address)

        context = get_group_tree(group.id)

        return render(request, 'manager/group.html', context)


def group_create(request):
    if request.method == 'POST':
        if request.POST['operation_type'] == 'create':
            name = request.POST['group_name']
            parent_id = int(request.POST['current_group_id'])
            parent = Group.objects.get(pk=parent_id)
            orga = parent.organization

            Group.objects.create(name=name, parent=parent, organization=orga)

            context = get_group_tree(parent_id)

        elif request.POST['operation_type'] == 'update':
            name = request.POST['group_name']
            group_id = int(request.POST['current_group_id'])
            group = Group.objects.get(pk=group_id)
            group.name = name
            group.save()

            context = get_group_tree(group_id)

        return render(request, 'manager/group.html', context)


def group_delete(request):
    if request.method == 'POST':
        group_id = int(request.POST['current_group_id'])
        group = Group.objects.get(pk=group_id)
        group_name = group.name
        parent_id = group.parent.id

        with transaction.atomic():
            for descendant in list(reversed(group.get_descendants(include_self=True))):
                for person in descendant.person_set.all():
                    person.user.delete()
                descendant.delete()
            group.delete()

        context = get_group_tree(parent_id)
        context['success_message'] = 'Le groupe %s a bien été supprimé.' % group_name

        return render(request, 'manager/group.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'manager/registration_form.html'

    #New Account
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #Process Form Data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('1')

        return render(request, self.template_name, {'form': form})