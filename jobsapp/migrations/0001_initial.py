# Generated by Django 3.2.8 on 2021-12-18 13:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(default='', max_length=254)),
                ('file', models.FileField(default='', null=True, upload_to='documents/%Y/%m/%d')),
                ('salary', models.CharField(blank=True, choices=[('under 3 million', 'Under 3 million'), ('3-5 million', '3-5 million'), ('5-10 million', '5-10 million'), ('10-15 million', '10-15 million'), ('15-25 million', '15-25 million'), ('upper 25 million', 'Upper 25 million')], default='', max_length=100, null=True)),
                ('location', models.CharField(choices=[('TP. HCM', 'TP. HCM'), ('Hà Nội', 'Hà Nội'), ('Đà Nẵng', 'Đà Nẵng'), ('Huế', 'Huế'), ('Bình Dương', 'Bình Dương'), ('Đồng Nai', 'Đồng Nai')], default='', max_length=150)),
                ('type', models.CharField(choices=[('1', 'Full time'), ('2', 'Part time'), ('3', 'Internship')], default='', max_length=10)),
                ('applicant', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(default='', max_length=150)),
                ('phone', models.CharField(max_length=10)),
                ('subject', models.CharField(default='', max_length=150)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('job_requirements', models.TextField(default='')),
                ('location', models.CharField(choices=[('TP. HCM', 'TP. HCM'), ('Hà Nội', 'Hà Nội'), ('Đà Nẵng', 'Đà Nẵng'), ('Huế', 'Huế'), ('Bình Dương', 'Bình Dương'), ('Đồng Nai', 'Đồng Nai')], max_length=150)),
                ('type', models.CharField(choices=[('1', 'Full time'), ('2', 'Part time'), ('3', 'Internship')], max_length=10)),
                ('last_date', models.DateField()),
                ('website', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('filled', models.BooleanField(default=False)),
                ('salary', models.CharField(blank=True, choices=[('under 3 million', 'Under 3 million'), ('3-5 million', '3-5 million'), ('5-10 million', '5-10 million'), ('10-15 million', '10-15 million'), ('15-25 million', '15-25 million'), ('upper 25 million', 'Upper 25 million')], default='', max_length=100, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('any', 'Any')], default='', max_length=30)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobsapp.category')),
                ('certificate', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jobsapp.certificate')),
                ('company', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='compa', to='accounts.company')),
                ('experience', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jobsapp.experience')),
            ],
        ),
        migrations.CreateModel(
            name='SaveJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='jobsapp.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='RequestApplicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate', to='jobsapp.applicant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.AddField(
            model_name='applicant',
            name='certificate',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jobsapp.certificate'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='experience',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jobsapp.experience'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='jobsapp.job'),
        ),
    ]
