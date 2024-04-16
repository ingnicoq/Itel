# Generated by Django 4.2.11 on 2024-04-11 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_comments_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='isdbt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('ip', models.CharField(max_length=20)),
                ('BR_min', models.FloatField(default=0.5)),
                ('canal_id', models.CharField(max_length=10)),
                ('estado', models.IntegerField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='megafax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('ip', models.CharField(max_length=20)),
                ('BR_min', models.FloatField(default=0.5)),
                ('canal_id', models.CharField(max_length=10)),
                ('estado', models.IntegerField(max_length=11)),
            ],
        ),
        migrations.DeleteModel(
            name='comments',
        ),
    ]