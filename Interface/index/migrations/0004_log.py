# Generated by Django 4.2.11 on 2024-04-17 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_isdbt_megafax_delete_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('min', models.IntegerField()),
                ('sec', models.IntegerField()),
                ('log', models.TextField(max_length=500)),
            ],
        ),
    ]