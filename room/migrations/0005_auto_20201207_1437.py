# Generated by Django 3.1.3 on 2020-12-07 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_user_id_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.room'),
        ),
    ]
