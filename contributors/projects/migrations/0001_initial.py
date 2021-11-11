# Generated by Django 3.2.9 on 2021-11-11 02:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150, unique=True)),
                ('description', models.TextField()),
                ('maximum_collaborators', models.PositiveSmallIntegerField()),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'deleted'), (1, 'active'), (2, 'completed')], db_index=True, default=1)),
                ('is_open', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('candidate_collaborators', models.ManyToManyField(blank=True, related_name='candidate_collaborators', to=settings.AUTH_USER_MODEL)),
                ('collaborators', models.ManyToManyField(blank=True, related_name='collaborators', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
