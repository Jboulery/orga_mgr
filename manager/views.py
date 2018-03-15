from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction
from django.http import JsonResponse

from .forms import RegistrationForm, LoginForm
from .models import Organization, Group, Person
from django.contrib.auth.models import User
import json


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


def person_index(request, person_id):
    person = get_object_or_404(Person, pk=int(person_id))
    context = get_group_tree(person.group.id)
    context['person'] = person
    return render(request, 'manager/person.html', context)


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
            parent_id = int(request.POST['selected_group_id'])
            parent = Group.objects.get(pk=parent_id)
            orga = parent.organization

            Group.objects.create(name=name, parent=parent, organization=orga)

            return group_index(request, parent_id)

        elif request.POST['operation_type'] == 'update':
            name = request.POST['group_name']
            group_id = int(request.POST['selected_group_id'])
            group = Group.objects.get(pk=group_id)
            group.name = name
            group.save()

            return group_index(request, group_id)


def group_delete(request):
    if request.method == 'POST':
        entities = json.loads(request.POST['to_delete_entities'])
        try:
            parent_id = Group.objects.get(pk=int(entities['groups'][0])).parent.id
        except:
            try:
                parent_id = Person.objects.get(pk=int(entities['persons'][0])).group.id
            except:
                return render(request, 'manager/group.html', get_group_tree(request.user.person.group.id))

        with transaction.atomic():
            for person_id in entities['persons']:
                person = Person.objects.get(pk=int(person_id))
                person.user.delete()
            for group_id in entities['groups']:
                group = Group.objects.get(pk=int(group_id))
                for descendant in list(reversed(group.get_descendants(include_self=True))):
                    for person in descendant.person_set.all():
                        person.user.delete()
                    descendant.delete()
                group.delete()

        context = get_group_tree(parent_id)
        context['success_message'] = 'Les éléments ont bien été supprimés.'

        return render(request, 'manager/group.html', context)


def group_moveto(request):
    if request.method == 'POST':
        entity = request.POST['entity']
        entity_id = int(request.POST['entity_id'])
        target_id = int(request.POST['target_id'])
        target = get_object_or_404(Group, pk=target_id)

        if entity == 'group':
            group = get_object_or_404(Group, pk=entity_id)
            group.move_to(target, position='last-child')
            group.save()
            response = JsonResponse({'success': True})
            return response

        elif entity == 'person':
            person = get_object_or_404(Person, pk=entity_id)
            person.group = target
            person.save()
            response = JsonResponse({'success': True})
            return response


class RegistrationFormView(View):
    form_class = RegistrationForm
    template_name = 'manager/registration_form.html'

    #New Account
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #Process Form Data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            with transaction.atomic():
                #Orga info
                orga_name = form.cleaned_data['orga_name']
                orga_activity = form.cleaned_data['orga_activity']
                orga_address = form.cleaned_data['orga_address']

                #User info
                user_firstname = form.cleaned_data['user_firstname']
                user_lastname = form.cleaned_data['user_lastname']
                user_email = form.cleaned_data['user_email'].lower()
                user_password = form.cleaned_data['user_password']
                user_conf_password = form.cleaned_data['user_confirmation_password']
                user_gender = form.cleaned_data['user_gender']
                user_dob = form.cleaned_data['user_date_of_birth']

                if user_password != user_conf_password:
                    return render(request, self.template_name, {'form': form, 'error_message': 'Les mots de passe ne correspondent pas !'})

                orga = Organization.objects.create(name=orga_name, activity=orga_activity, address=orga_address)
                group = Group.objects.create(name=orga_name, organization=orga)

                username = user_email
                password = User.objects.make_random_password()

                user = User.objects.create_user(username=username, password=password, email=user_email,
                                                first_name=user_firstname, last_name=user_lastname)
                user.set_password(user_password)
                user.save()
                person = Person.objects.create(user=user, group=group, is_manager=True, is_admin=True,
                                               gender=user_gender, date_of_birth=user_dob)

                user = authenticate(username=username, password=user_password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        context = get_group_tree(group.id)
                        return render(request, 'manager/group.html', context)
                    else:
                        return render(request, self.template_name,
                                      {'form': form, 'error_message': 'Votre compte est désactivé, veuillez contacter un administrateur du site'})

        return render(request, self.template_name,
                      {'form': form, 'error_message': "Les informations fournies n'ont pas permis de vous enregistrer"})


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'manager/login_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['login_user_email']
            password = form.cleaned_data['login_user_password']

            user = authenticate(username=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    group = user.person.group
                    context = get_group_tree(group.id)
                    return render(request, 'manager/group.html', context)
                else:
                    return render(request, self.template_name,
                                  {'form': form, 'error_message': 'Votre compte est désactivé, veuillez contacter un administrateur du site'})

        return render(request, self.template_name,
                      {'form': form, 'error_message': "Les informations fournies sont incorrectes"})