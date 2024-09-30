from django.shortcuts import render
from django.views.generic.base import TemplateView

from portal.views.base import BasePublicContext


class Home(TemplateView, BasePublicContext):
    template_name = "public/index.html"


class About(TemplateView, BasePublicContext):
    template_name = "public/about.html"


class Gallery(TemplateView, BasePublicContext):
    template_name = "public/gallery.html"


class Contact(TemplateView, BasePublicContext):
    template_name = "public/contact.html"


class Page404(TemplateView):
    template_name = "public/404.html"
