from django.conf.urls import url

from project.models.main.solver import get_solution
from project.models.main.views import main_page_view

urlpatterns = [
    url(r'^$', main_page_view, name='main_page_view'),
    url(r'^solve/$', get_solution, name='get_solution'),
]
