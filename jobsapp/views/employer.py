from django.http import Http404, request
from django.contrib.auth.decorators import login_required
from django.db.models import query
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm, SaveApplicantForm
from accounts.forms import RegistrationForm, CreateCompanyForm, UpdateCompanyForm
from accounts.models import Company, User
from jobsapp.decorators import user_is_employer
from jobsapp.models import Applicant, Certificate, Experience, Job, RequestApplicant, Category
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone



class DashboardView(ListView):
    model = Job
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(company_id=self.request.user.company.id)


class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants-job.html'
    context_object_name = 'applicants'
    paginate_by = 5

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs['job_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context


class JobCreateView(CreateView):
    template_name = 'jobs/create.html'
    form_class = CreateJobForm
    extra_context = {
        'title': 'Post New Job'
    }
    success_url = reverse_lazy('jobs:employer-dashboard')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ApplicantsListView(ListView):
    model = Applicant
    template_name = 'jobs/employer/all-applicants.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        return Applicant.objects.filter(job__company_id=self.request.user.company.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.all()
        context['certificates'] = Certificate.objects.all()
        context['categories'] = Category.objects.all()
        return context


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_employer
def filled(request, job_id=None):
    job = Job.objects.get(company_id=request.user.company.id, id=job_id)
    job.filled = True
    job.save()
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))


class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy('jobs:employer-dashboard')

    def get_object(self):
        id = self.kwargs.get("id")
        messages.info(self.request, 'Successfully delete for the job!')
        return get_object_or_404(Job, id=id)


class JobUpdateView(UpdateView):
    model = Job
    template_name = 'jobs/update.html'
    form_class = CreateJobForm
    success_url = reverse_lazy('jobs:employer-dashboard')

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Job, id=id)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("jobs:employer-dashboard" )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
@user_is_employer
def profile_employer(request):
    if request.method == 'POST':
        u_form = RegistrationForm(request.POST, instance=request.user)
        p_form = UpdateCompanyForm(request.POST,
                                   request.FILES,
                                   instance=request.user.company) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('/') 

    else:
        u_form = RegistrationForm(instance=request.user)
        p_form = UpdateCompanyForm(instance=request.user.company)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'jobs/employer/edit-profile.html', context)   
    

class ApplicantDetailsView(DetailView):
    model = Applicant
    template_name = 'jobs/employer/applicant-details.html'
    context_object_name = 'applicant'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(ApplicantDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Applicant doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("Applicant doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ApplicantSave(CreateView):
    model = RequestApplicant
    form_class = SaveApplicantForm
    slug_field = 'applicant_id'
    slug_url_kwarg = 'applicant_id'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully save for the applicant!')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('jobs:home'))

    def get_success_url(self):
        return reverse_lazy('jobs:employer-all-applicants')

    def form_valid(self, form):
        applicant = RequestApplicant.objects.filter(user_id=self.request.user.id, applicant_id=self.kwargs['applicant_id'])
        if applicant:
            messages.info(self.request, 'Successfully save for the applicant!')
            return HttpResponseRedirect(self.get_success_url())
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ListApplicantSave(ListView):
    model = RequestApplicant
    template_name = 'jobs/employer/applicant-save.html'
    context_object_name = 'candidates'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class ApplicantSaveDelete(DeleteView):
    model = RequestApplicant
    success_url = reverse_lazy('jobs:all-candidate-save')

    def get_object(self):
        id = self.kwargs.get("id")
        messages.info(self.request, 'Successfully delete for the job application!')
        return get_object_or_404(RequestApplicant, id=id)



class ApplicantByExperience(ListView):
    slug_url_kwarg = 'experience_id'
    template_name = 'jobs/employer/applicant-experience.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        query = Applicant.objects.filter(experience_id=self.kwargs['experience_id']).order_by('id')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.all()
        context['certificates'] = Certificate.objects.all()
        context['categories'] = Category.objects.all()
        return context


class ApplicantByCertificate(ListView):
    slug_url_kwarg = 'certificate_id'
    template_name = 'jobs/employer/applicant-experience.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        query = Applicant.objects.filter(certificate_id=self.kwargs['certificate_id']).order_by('id')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.all()
        context['certificates'] = Certificate.objects.all()
        context['categories'] = Category.objects.all()
        return context


class ApplicantByCategory(ListView):
    slug_url_kwarg = 'category_id'
    template_name = 'jobs/employer/applicant-experience.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        query = Applicant.objects.filter(job__category_id=self.kwargs['category_id']).order_by('id')
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.all()
        context['certificates'] = Certificate.objects.all()
        context['categories'] = Category.objects.all()
        return context