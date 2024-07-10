# Generated by Django 5.0.4 on 2024-05-23 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentAffairs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('link', models.URLField()),
                ('text', models.TextField()),
                ('image', models.ImageField(upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExcelData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(upload_to='excel_files/')),
            ],
        ),
        migrations.CreateModel(
            name='MockTestSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mock_test_number', models.IntegerField(unique=True)),
                ('solution_file', models.FileField(upload_to='mock_test_solutions/')),
            ],
        ),
        migrations.CreateModel(
            name='StudyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pdf_file', models.FileField(upload_to='study_plans/')),
            ],
        ),
        migrations.CreateModel(
            name='UserLoginActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('login_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
