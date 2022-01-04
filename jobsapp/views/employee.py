from django.contrib.auth import models
from django.contrib.auth.decorators import login_required
from django.http import Http404, request
from django.utils import timezone
from django.urls.base import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, ListView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, DeleteView
from accounts.forms import ActionForm, EmployeeUpdateForm, RegistrationForm
from accounts.models import Action, Comment, Company, User
from jobsapp.decorators import user_is_employee
from jobsapp.forms import ApplyJobForm, CommentForm, SaveJobForm
from jobsapp.models import Applicant, Job, RequestApplicant, SaveJob
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect


@login_required
@user_is_employee
def profile_employee(request):
    if request.method == 'POST':
        u_form = RegistrationForm(request.POST, instance=request.user)
        p_form = EmployeeUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.employee) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('/') 

    else:
        u_form = RegistrationForm(instance=request.user)
        p_form = EmployeeUpdateForm(instance=request.user.employee)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'jobs/employee/edit-profile.html', context)  


class JobApply(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    template_name = 'jobs/employee/apply-job.html'
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employee':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JobApply, self).get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, id = self.kwargs['job_id'])
        return context

    def form_valid(self, form):
        form.instance.applicant = self.request.user.employee
        form.instance.job = get_object_or_404(Job, id = self.kwargs['job_id'])
        return super(JobApply, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'You already applied for this job')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('jobs:jobs-detail', kwargs={'id': self.kwargs['job_id']})



class CVListView(ListView):
    model = Applicant
    template_name = 'jobs/employee/all-applicants.html'
    context_object_name = 'applicants'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(applicant_id=self.request.user.employee.id)


class CommentListView(ListView):
    model = Comment
    template_name = 'companys/company-jobs.html'
    context_object_name = 'comments'
    pk_url_kwarg = 'id'
    slug_url_kwarg = 'company_id'
    paginate_by = 5

    def get_queryset(self):
        return Comment.objects.filter(company_id=self.kwargs['company_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(id=self.kwargs['company_id'])
        context['jobs'] = Job.objects.filter(company_id=self.kwargs['company_id'])
        return context


class JobByCompany(ListView):
    model = Job
    template_name = 'companys/company-jobs.html'
    context_object_name = 'jobs'
    pk_url_kwarg = 'id'
    slug_url_kwarg = 'company_id'

    def get_queryset(self):
        return Job.objects.filter(company_id=self.kwargs['company_id'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(id=self.kwargs['company_id'])
        context['comments'] = Comment.objects.filter(company_id=self.kwargs['company_id'])
        return context


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'companys/add-comment.html'
    success_url = reverse_lazy('jobs:companys')


    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employee':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Comment, id=id)

    def form_valid(self, form):
        form.instance.employee = self.request.user.employee
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("jobs:companys" )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'You already update for this review')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



def addcomment(request, id): 
    url = request.META.get('HTTP_REFERER') 
    if request.method == "POST": 
        form = CommentForm(request.POST)
        if form.is_valid(): 
            data = Comment() 
            data.rating = form.cleaned_data['rating'] 
            data.comment = form.cleaned_data['comment'] 
            data.ip = request.META.get('REMOTE_ADDR') 
            data.company_id = id
            data.employee_id= request.user.employee.id
            data.save() 
            messages.success(request, "Thank you! Your review has been submitted.") 
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


class JobSave(CreateView):
    model = SaveJob
    form_class = SaveJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully save for the job!')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('jobs:home'))


    def get_success_url(self):
        return reverse_lazy('jobs:jobs-detail', kwargs={'id': self.kwargs['job_id']})


    def form_valid(self, form):
        job = SaveJob.objects.filter(user_id=self.request.user.id, job_id=self.kwargs['job_id'])
        if job:
            messages.info(self.request, 'Successfully save for the job!')
            return HttpResponseRedirect(self.get_success_url())
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ListJobSave(ListView):
    model = SaveJob
    template_name = 'jobs/employee/job-save.html'
    context_object_name = 'works'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class JobSaveDelete(DeleteView):
    model = SaveJob
    success_url = reverse_lazy('jobs:all-job-save')

    def get_object(self):
        id = self.kwargs.get("id")
        messages.info(self.request, 'Successfully delete for the saved job!')
        return get_object_or_404(SaveJob, id=id)


class CommentDelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('jobs:companys')

    def get_object(self):
        id = self.kwargs.get("id")
        messages.info(self.request, 'Successfully delete for the review!')
        return get_object_or_404(Comment, id=id)

