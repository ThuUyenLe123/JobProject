from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import query
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from accounts.models import Comment, Company
from jobsapp.forms import ApplyJobForm, ContactForm
from jobsapp.models import Applicant, Category, Contact, Job, Experience, Certificate
from jobsapp.decorators import user_is_employee
from django.urls import reverse, reverse_lazy
from django.db.models.aggregates import Count


class HomeView(ListView):
    model = Job
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = self.model.objects.filter(last_date__range=[timezone.now(), "2080-12-31"])[:6]
        context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        return context


def about_us(request):
    return render(request, "jobs/about.html", {})


class SearchView(ListView):
    model = Job
    template_name = 'jobs/search.html'
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['experiences'] = Experience.objects.all()
        context['certificates'] = Certificate.objects.all()
        return context

    def get_queryset(self):
        return self.model.objects.filter(company__location__contains=self.request.GET['location'],
                                         title__contains=self.request.GET['position'])

 

class JobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['experiences'] = Experience.objects.all()
        context['certificates'] = Certificate.objects.all()
        context['jobs'] = self.model.objects.filter(last_date__range=[timezone.now(), "2080-12-31"])
        return context


class JobDetailsView(DetailView):
    model = Job
    template_name = 'jobs/details.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'
    template_name = 'jobs/employee/apply-job.html'
    success_url = reverse_lazy('jobs:home')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('jobs:jobs-detail', kwargs={'id': self.kwargs['job_id']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.job_id = Job.objects.get(id=self.kwargs.get('id'))
        return super(ApplyJobView, self).form_valid(form)

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(user_id=self.request.user.id, job_id=self.kwargs['job_id'])
        if applicant:
            messages.info(self.request, 'You already applied for this job')
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'jobs/contact.html'
    success_url = reverse_lazy("jobs:contact")


    def form_valid(self, form):
        return super(ContactCreateView, self).form_valid(form)
        

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully send for the request! Thank you very much')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CompanyListView(ListView):
    model = Company
    template_name = 'companys/company-list.html'
    context_object_name = 'companys'
    paginate_by = 8

    def countJob(self):
        jobs = Job.objects.filter(company=self).aggregate(count=Count('id'))
        count = 0
        if jobs['count'] is not None:
            count = int(jobs['count'])
        return count



class JobByCategory(ListView):
    slug_url_kwarg = 'category_id'
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['experiences'] = Experience.objects.all()
        context['certificates'] = Certificate.objects.all()
        return context

    def get_queryset(self):
        return Job.objects.filter(category_id=self.kwargs['category_id'], last_date__range=[timezone.now(), "2080-12-31"]).order_by('id')


class JobByCertificate(ListView):
    slug_url_kwarg = 'certificate_id'
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(certificate_id=self.kwargs['certificate_id'], last_date__range=[timezone.now(), "2080-12-31"]).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['experiences'] = Experience.objects.all()
        context['certificates'] = Certificate.objects.all()
        return context


class JobByExperience(ListView):
    slug_url_kwarg = 'experience_id'
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(experience_id=self.kwargs['experience_id'], last_date__range=[timezone.now(), "2080-12-31"]).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['experiences'] = Experience.objects.all()
        context['certificates'] = Certificate.objects.all()
        return context
    



