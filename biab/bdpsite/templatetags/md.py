from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape as escape
import markdown

register = template.Library()

@register.filter("markdown")
def markdown_filter(s):
  return mark_safe(markdown.markdown(escape(s)))
