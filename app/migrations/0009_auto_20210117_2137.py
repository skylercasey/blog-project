# Generated by Django 3.1.4 on 2021-01-17 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_myuser_f_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='f_name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(default='none', max_length=100),
        ),
    ]
