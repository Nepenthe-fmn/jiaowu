# Generated by Django 2.2.4 on 2019-11-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_student_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='cls',
        ),
        migrations.AddField(
            model_name='teacher',
            name='cls',
            field=models.ManyToManyField(to='app01.classes'),
        ),
    ]
