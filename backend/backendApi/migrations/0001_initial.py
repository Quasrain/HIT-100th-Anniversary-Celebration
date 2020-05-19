# Generated by Django 3.0.6 on 2020-05-12 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('UID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=50)),
                ('Tag', models.CharField(max_length=50)),
                ('Comment', models.CharField(max_length=500)),
                ('Year', models.IntegerField()),
                ('Checked', models.BooleanField(default=False)),
                ('Count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'comment',
            },
        ),
    ]
