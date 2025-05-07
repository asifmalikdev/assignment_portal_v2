from django import template
from assignments.forms import AssignmentQuestionInLineForm

register = template.Library()

@register.filter
def with_instance(form, instance):
    return AssignmentQuestionInLineForm(instance=instance, user=instance.teacher)
