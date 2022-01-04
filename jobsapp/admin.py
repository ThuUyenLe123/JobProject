from django.contrib import admin
from jobsapp.models import  Applicant, Employee, Company, Contact, Job, Category, Experience, Certificate


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'email', "salary", "experience", "certificate", 'file')
    list_filter = ["salary", "experience", "certificate", 'job']
    search_fields = ['email', 'applicant' ]

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "dob", "location", "phone_number")
    list_filter =  ['gender', 'location']
    search_fields = ['gender', 'location', "phone_number"]

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "amount", "location", "phone_number")
    list_filter =  ["location", "amount"]
    search_fields = ["amount", 'location', "phone_number"]


class JobAdmin(admin.ModelAdmin):
    list_display = ("company", "category", "title", "last_date", "salary", "experience", "certificate")
    list_filter = ['last_date', "salary", "experience", "certificate", "category"]
    search_fields = ['title']


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'subject', 'message', 'phone')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Category)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Experience)
admin.site.register(Certificate)

