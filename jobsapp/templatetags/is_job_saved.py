from django import template
from jobsapp.models import SaveJob

register = template.Library()


@register.simple_tag(name='is_job_saved')
def is_job_saved(job, user):
    saved = SaveJob.objects.filter(job=job, user=user)
    if saved:
        return True
    else:
        return False