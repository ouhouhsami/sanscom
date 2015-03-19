from django import template
register = template.Library()


def pager(context, max_pages=10):
    if context['is_paginated']:
        if len(context['paginator'].page_range) > max_pages:
            number = context['page_obj'].number
            last = context['paginator'].num_pages
            if number <= max_pages / 2 + 1:
                context['paginator_page_range'] = context['paginator'].page_range[0:max_pages]
            elif number > max_pages / 2 + 1 and number < last - max_pages / 2:
                context['paginator_page_range'] = context['paginator'].page_range[number-max_pages/2-1:number+max_pages/2-1]
            else:
                context['paginator_page_range'] = context['paginator'].page_range[last-max_pages:last]
        else:
            context['paginator_page_range'] = context['paginator'].page_range
    return context
# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('widgets/pager.html', takes_context=True)(pager)
