# Generated by Django 4.2.20 on 2025-03-14 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.CharField(default='NTF-171432b9', max_length=20, primary_key=True, serialize=False),
        ),
    ]
