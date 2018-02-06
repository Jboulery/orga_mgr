from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    activity = models.CharField(max_length=500, default='')
    address = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.name


class Group(MPTTModel):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    GENDER_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=500, default='')
    picture = models.URLField(default='', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()