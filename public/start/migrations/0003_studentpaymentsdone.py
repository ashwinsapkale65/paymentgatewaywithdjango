# Generated by Django 4.0.6 on 2022-07-14 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0002_rename_studentspaymentpending_studentpaymentremaining'),
    ]

    operations = [
        migrations.CreateModel(
            name='studentpaymentsdone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=122)),
                ('city', models.CharField(max_length=122)),
                ('number', models.CharField(max_length=122)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
    ]