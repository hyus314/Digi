# Generated by Django 5.0.1 on 2024-03-04 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DigiUser',
        ),
    ]
