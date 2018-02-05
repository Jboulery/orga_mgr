from django.contrib import admin

from .models import Organization, Group, Person

admin.site.register(Organization)
admin.site.register(Group)
admin.site.register(Person)
