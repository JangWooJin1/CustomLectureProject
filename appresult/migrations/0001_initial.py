# Generated by Django 4.1.6 on 2023-08-21 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appsearch', '0001_initial'),
        ('appaccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyTimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_num', models.IntegerField()),
                ('lecture_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsearch.lecture')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appaccount.user')),
            ],
        ),
        migrations.AddConstraint(
            model_name='mytimetable',
            constraint=models.UniqueConstraint(fields=('user_id', 'lecture_id', 'class_num'), name='unique_time_table'),
        ),
    ]
