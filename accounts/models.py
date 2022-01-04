from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.urls.base import reverse
from django.db.models import Avg, Count
from PIL import Image


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('any', 'Any'))

LOCATION_CHOICES = (
    ('TP. HCM', 'TP. HCM'),
    ('Hà Nội', 'Hà Nội'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Huế', 'Huế'),
    ('Bình Dương', 'Bình Dương')
)

ROLE_CHOICES = (
    ('I am the owner of this business', 'I am the owner of this business' ),
    ('I am the employee of this company', 'I am the employee of this company'),
    ('I am a recruiter for this business', 'I am a recruiter for this business'),
)

AMOUNT = (
    ('Less than 5 employees','Less than 5 employees'),
    ('6 to 50 employees','6 to 50 employees'),
    ('51 to 200 employees', '51 to 200 employees'),
    ('More than 200 employees', 'More than 200 employees')
)

MARITAL_CHOICES = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Widowed', 'Widowed'),
    ('Divorced', 'Divorced'),
    ('Separated', 'Separated')
)

ACTION_CHOICES = (
    ('Like', 'Like'),
    ('Dislike', 'Dislike')
)


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.get_full_name()

    def __str__(self):
        return self.email

    objects = UserManager()


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    image = models.ImageField(null=True,  default="images/images.jpg", upload_to='images')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="")
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default="")
    marital_status = models.CharField(max_length=50, choices=MARITAL_CHOICES, default="")
    phone_number = PhoneNumberField(blank=False, unique=True, null=True)
    dob = models.DateField(null=True)

    def __str__(self):
        return self.user.get_full_name()



class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    company_name = models.CharField(max_length=100, default="")
    company_description = models.TextField(blank=True, null=True, default="")
    role = models.CharField(choices=ROLE_CHOICES, max_length=50, default="") 
    image = models.ImageField(null=True,  default="images/images.jpg", upload_to='images')
    amount = models.CharField(choices=AMOUNT, max_length=50, default="") 
    address = models.CharField(max_length=100, default="")
    website = models.URLField(max_length=200, default="")
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default="")
    phone_number = PhoneNumberField(blank=False, unique=True, null=True)

    def __str__(self):
        return self.company_name


    def averageReview(self):
        reviews = Comment.objects.filter(company=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = Comment.objects.filter(company=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image
        
        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) 


class Comment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default="2")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companys')
    created_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    status = models.BooleanField(default=True)
    rating = models.FloatField(null=True)
    ip = models.CharField(max_length=20, blank=True)
    

class Action(models.Model):
    user = models.ForeignKey(User, blank=True, related_name="user", on_delete=models.CASCADE)
    type = models.CharField(choices=ACTION_CHOICES, default="Like", max_length=20)
    comment = models.ForeignKey(Comment, blank=True, on_delete=models.CASCADE)
    
