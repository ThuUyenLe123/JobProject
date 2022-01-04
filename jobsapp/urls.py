from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import ListView


  


app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='searh'),
    path('employer/dashboard/', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
        path('experience/<int:experience_id>/applicants', ApplicantByExperience.as_view(), name='experience-applicants'),
        path('certificate/<int:certificate_id>/applicants', ApplicantByCertificate.as_view(), name='certificate-applicants'),
        path('category/<int:category_id>/applicants', ApplicantByCategory.as_view(), name='category-applicants'),
        
    ])),
    path('apply-job/<int:job_id>', JobApply.as_view(), name='apply-job'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('jobs/<int:id>', JobDetailsView.as_view(), name='jobs-detail'),
    path('employer/jobs/create', JobCreateView.as_view(), name='employer-jobs-create'),
    path('employer/jobs/delete/<int:id>', JobDeleteView.as_view(), name='employer-jobs-delete'),
    path('employer/jobs/update/<int:id>', JobUpdateView.as_view(), name='employer-jobs-update'),
    path('contact', ContactCreateView.as_view(), name ='contact'),
    path('employee/all-applicants', CVListView.as_view(), name='employee-all-applicants'),
    path('about', about_us, name= 'about'),
    path('companys', CompanyListView.as_view(), name='companys'),
    path('employer/profile/update', profile_employer, name='employer-profile-update'),
    path('company/<int:company_id>/jobs', JobByCompany.as_view(), name='company-jobs'),
    path('category/<int:category_id>/jobs', JobByCategory.as_view(), name='category-jobs'),
    path('experience/<int:experience_id>/jobs', JobByExperience.as_view(), name='experience-jobs'),
    path('certificate/<int:certificate_id>/jobs', JobByCertificate.as_view(), name='certificate-jobs'),
    path('comment/<int:id>/add', addcomment, name='addcomment'),
    path('applicants/<int:id>', ApplicantDetailsView.as_view(), name='applicant-details'),
    path('applicant/save/<int:applicant_id>', ApplicantSave.as_view(), name='applicant-save'),
    path('job/save/<int:job_id>', JobSave.as_view(), name='job-save'),
    path('all-job/save', ListJobSave.as_view(), name='all-job-save'),
    path('all-candidate/save', ListApplicantSave.as_view(), name='all-candidate-save'),
    path('candidate-save/remove/<int:id>', ApplicantSaveDelete.as_view(), name='candidate-save-remove'),
    path('job-save/remove/<int:id>', JobSaveDelete.as_view(), name='job-save-remove'),
    path('comment/delete/<int:id>', CommentDelete.as_view(), name='comment-delete'),
    path('comment/<int:id>/edit', CommentUpdate.as_view(), name='comment-update'),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)