from django.shortcuts import render

from project.core.utilities.constants import Constants


def main_page_view(request):
    constants = Constants()
    return render(request, 'main.html', locals())
