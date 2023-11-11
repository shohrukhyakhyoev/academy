from django.shortcuts import render
from django.shortcuts import render
from course.models import Course

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def paginate_objects(request, queryset, num):
    paginator = Paginator(queryset, num)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return queryset


def tutorials(request):
    subjects = Course.objects.order_by('-timestamp')

    search_request_var = 'q'
    search_query = request.GET.get(search_request_var, '')
    if search_query:
        subjects = subjects.filter(
            Q(title__icontains=search_query) |
            Q(category__title__icontains=search_query)
        ).distinct()

    subjects = paginate_objects(request, subjects, 6)

    context = {
        'tutorials': subjects,
        'page_request_var': 'page',
        'search_request_var': search_request_var,
        'search_query': search_query,
    }

    return render(request, 'course/tutorials.html', context)
