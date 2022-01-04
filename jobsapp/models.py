from os import name
from django.db import models
from django.db.models.aggregates import Count
from django.utils import timezone
from django.urls.base import reverse
from accounts.models import Company, Employee, User
from django.db.models import Func, Sum

JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('any', 'Any'))


SALARY_CHOICES = (
    ('under 3 million', 'Under 3 million'),
    ('3-5 million', '3-5 million' ),
    ('5-10 million', '5-10 million' ),
    ('10-15 million', '10-15 million' ),
    ('15-25 million', '15-25 million' ),
    ('upper 25 million', 'Upper 25 million' ),
)

LOCATION_CHOICES = (
    ('TP. HCM', 'TP. HCM'),
    ('Hà Nội', 'Hà Nội'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Huế', 'Huế'),
    ('Bình Dương', 'Bình Dương'),
    ('Đồng Nai', 'Đồng Nai')
)


class Certificate(models.Model):
    certificate = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.certificate

class Experience(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Job(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    job_requirements = models.TextField(default="")
    location = models.CharField(max_length=150, choices=LOCATION_CHOICES)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    last_date = models.DateField()
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, default=1)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, default=1)
    salary = models.CharField(max_length=100, null=True, blank=True, default="", choices=SALARY_CHOICES)
    gender = models.CharField( max_length=30, default="", choices=GENDER_CHOICES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="compa", default="")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail",kwargs={'id':self.job_id,'job':self.job})

    

class SaveJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="jobs")
    created_at = models.DateTimeField(default=timezone.now)


class Applicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, default=1)
    applicant = models.ForeignKey(Employee, on_delete=models.CASCADE, default="")
    created_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50, default="")
    email = models.EmailField( default="")
    file = models.FileField(null=True,  default="", upload_to='documents/%Y/%m/%d')
    salary = models.CharField(max_length=100, null=True, blank=True, default="", choices=SALARY_CHOICES)
    location = models.CharField(max_length=150, default="", choices=LOCATION_CHOICES)
    type = models.CharField(choices=JOB_TYPE, max_length=10, default="")
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, default=1)


class RequestApplicant(models.Model):
    filled = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="candidate")
    created_at = models.DateTimeField(default=timezone.now)


class Contact(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, default="")
    phone = models.CharField(max_length=10)
    subject = models.CharField(max_length=150, default="")
    message = models.TextField()

    def __str__(self):
        return self.full_name

