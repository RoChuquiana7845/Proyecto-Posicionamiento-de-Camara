# Generated by Django 4.2.6 on 2023-12-27 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camaras', '0009_sensores_imagen_alter_sensores_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='camara',
            name='alcance',
            field=models.IntegerField(default=0),
        ),
    ]