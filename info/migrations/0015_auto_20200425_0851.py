# Generated by Django 2.2.5 on 2020-04-25 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0014_attendanceclass_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assigntime',
            name='period',
            field=models.CharField(choices=[('8:30 - 10:00', '8:30 - 10:00'), ('10:00 - 11:30', '10:00 - 11:30'), ('11:30 - 1:00', '11:30 - 1:00'), ('2:00 - 3:30', '2:00 - 3:30'), ('3:30 - 5:00', '3:30 - 5:00')], default='11:00 - 11:50', max_length=50),
        ),
    ]