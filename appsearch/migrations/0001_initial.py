# Generated by Django 4.1.6 on 2023-08-14 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appaccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('lecture_id', models.IntegerField(primary_key=True, serialize=False)),
                ('lecture_curriculum', models.CharField(max_length=10)),
                ('lecture_classification', models.CharField(blank=True, max_length=15, null=True)),
                ('lecture_code', models.CharField(max_length=8)),
                ('lecture_number', models.CharField(max_length=5)),
                ('lecture_name', models.CharField(max_length=100)),
                ('lecture_professor', models.CharField(blank=True, max_length=15, null=True)),
                ('lecture_campus', models.CharField(blank=True, max_length=5, null=True)),
                ('lecture_credit', models.IntegerField()),
                ('lecture_univ', models.CharField(blank=True, max_length=15, null=True)),
                ('lecture_major', models.CharField(blank=True, max_length=50, null=True)),
                ('lecture_remark', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserBasket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsearch.lecture')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appaccount.user')),
            ],
        ),
        migrations.CreateModel(
            name='LectureTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_day', models.CharField(blank=True, max_length=4, null=True)),
                ('lecture_start_time', models.FloatField(blank=True, null=True)),
                ('lecture_end_time', models.FloatField(blank=True, null=True)),
                ('lecture_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsearch.lecture')),
            ],
        ),
        migrations.CreateModel(
            name='LectureRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_room', models.CharField(blank=True, max_length=50, null=True)),
                ('lecture_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsearch.lecture')),
            ],
        ),
        migrations.AddConstraint(
            model_name='lecture',
            constraint=models.UniqueConstraint(fields=('lecture_code', 'lecture_number'), name='unique_lecture'),
        ),
        migrations.AddConstraint(
            model_name='userbasket',
            constraint=models.UniqueConstraint(fields=('user_id', 'lecture_id'), name='unique_basket'),
        ),
    ]