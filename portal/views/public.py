from django.shortcuts import render
from django.views.generic.base import TemplateView


class Home(TemplateView):
    template_name = 'public/index.html'


class About(TemplateView):
    template_name = 'public/about.html'


class Gallery(TemplateView):
    template_name = 'public/gallery.html'

class Contact(TemplateView):
    template_name = 'public/contact.html'