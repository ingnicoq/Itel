# Generated by Django 4.2.11 on 2024-04-17 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('min', models.IntegerField()),
                ('sec', models.IntegerField()),
                ('canal_id', models.CharField(max_length=30)),
                ('BR', models.IntegerField()),
            ],
        ),
    ]