from django.shortcuts import render

from project.core.data.initial import InitialData


def main_page_view(request):
    initial = InitialData()
    return render(request, 'main.html', locals())
