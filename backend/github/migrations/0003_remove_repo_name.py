# Generated by Django 3.0.2 on 2020-02-23 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0002_repo_base_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repo',
            name='name',
        ),
    ]
