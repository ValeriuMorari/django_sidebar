from django.shortcuts import render
from django.views.generic import TemplateView


class MainDashboard(TemplateView):
    login_url = "/login/"
    template_name = "index.html"
