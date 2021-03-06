# Generated by Django 2.0.2 on 2018-02-03 00:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('activity', models.CharField(default='', max_length=500)),
                ('address', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_manager', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('gender', models.CharField(choices=[('M', 'Homme'), ('F', 'Femme')], max_length=1)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(default='', max_length=500)),
                ('picture', models.URLField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='manager.Group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Organization'),
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='manager.Group'),
        ),
    ]
