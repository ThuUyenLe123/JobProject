from django import template

from jobsapp.models import RequestApplicant, Category

register = template.Library()


@register.simple_tag(name='is_already_saved')
def is_already_saved(applicant, user):
    saved = RequestApplicant.objects.filter(applicant=applicant, user=user)
    if saved:
        return True
    else:
        return False


@register.inclusion_tag('jobs/jobs.html', name='show_categorys')
def show_categorys():
      obj = Category.objects.values_list('category', flat=True)
      return {'categories': obj}