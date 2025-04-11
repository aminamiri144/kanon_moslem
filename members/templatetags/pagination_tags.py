from django import template
from django.utils.http import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def page_url(context, page_number):
    """
    Generates URL for a given page, preserving current GET parameters.
    """
    request = context['request']
    # ایجاد یک dictionary از querystring
    querydict = request.GET.copy()

    # حذف پارامتر page قبلی
    if 'page' in querydict:
        querydict.pop('page')

    querydict['page'] = page_number

    # ساختن URL جدید با تمام پارامترهای GET
    url = f"{request.path}?{querydict.urlencode()}"

    return url


@register.simple_tag
def smart_pagination(page_obj, window=2, edge=1):
    """
    Generates a smart pagination range with ellipsis (represented by None)
    - window: number of pages around current page
    - edge: number of pages to always show at beginning and end
    """
    current = page_obj.number
    total = page_obj.paginator.num_pages

    pages = set()

    # always show first edge pages
    pages.update(range(1, edge + 1))

    # always show last edge pages
    pages.update(range(total - edge + 1, total + 1))

    # always show window around current page
    pages.update(range(current - window, current + window + 1))

    # filter out invalid pages
    valid_pages = [p for p in sorted(pages) if 1 <= p <= total]

    # insert None between gaps (will be rendered as '...')
    result = []
    prev = None
    for p in valid_pages:
        if prev is not None and p - prev > 1:
            result.append(None)  # gap
        result.append(p)
        prev = p

    return result
