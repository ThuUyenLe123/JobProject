from django import forms
from django.db import models
from django.forms import fields
from django.forms.widgets import DateInput
from django.conf import settings 
from jobsapp.models import Applicant, Contact, Job, RequestApplicant, SaveJob
from accounts.models import Comment, Company


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateJobForm(forms.ModelForm):
    last_date = forms.DateField(widget=DateInput)
    class Meta:
        model = Job
        exclude = ('company', 'created_at', 'filled', 'location' )

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job

    def __init__(self, *args, **kwargs):
        super(CreateJobForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = "Job Title"
        self.fields['description'].label = "Job Description"


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = ('job', 'created_at', 'applicant', 'user')
    

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def is_valid(self):
        valid = super(ContactForm, self).is_valid()
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        contact = super(ContactForm, self).save(commit=False)
        if commit:
            contact.save()
        return contact


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('rating', 'comment')


class SaveApplicantForm(forms.ModelForm):
    class Meta:
        model = RequestApplicant
        fields = ('applicant', 'filled')    


class SaveJobForm(forms.ModelForm):
    class Meta:
        model = SaveJob
        fields = ('job',)  