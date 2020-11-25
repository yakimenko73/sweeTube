# Generated by Django 3.1.2 on 2020-11-25 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=0, max_length=8, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('host', models.CharField(max_length=50, unique=True)),
                ('moder_can_add', models.BooleanField(default=False)),
                ('moder_can_remove', models.BooleanField(default=False)),
                ('moder_can_move', models.BooleanField(default=False)),
                ('moder_can_playpause', models.BooleanField(default=False)),
                ('moder_can_seek', models.BooleanField(default=False)),
                ('moder_can_skip', models.BooleanField(default=False)),
                ('moder_can_use_chat', models.BooleanField(default=False)),
                ('moder_can_kick', models.BooleanField(default=False)),
                ('quest_can_add', models.BooleanField(default=False)),
                ('quest_can_remove', models.BooleanField(default=False)),
                ('quest_can_move', models.BooleanField(default=False)),
                ('quest_can_playpause', models.BooleanField(default=False)),
                ('quest_can_seek', models.BooleanField(default=False)),
                ('quest_can_skip', models.BooleanField(default=False)),
                ('quest_can_use_chat', models.BooleanField(default=False)),
                ('quest_can_kick', models.BooleanField(default=False)),
            ],
        ),
    ]
