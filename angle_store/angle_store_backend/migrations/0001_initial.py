# Generated by Django 3.2.4 on 2021-06-10 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('price', models.IntegerField()),
                ('start_date', models.CharField(max_length=10)),
            ],
        ),
    ]
