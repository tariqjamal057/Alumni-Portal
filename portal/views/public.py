from django.shortcuts import render
from django.views.generic.base import TemplateView

from portal.utils import is_alumni


class BasePublicContext(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_alumni"] = is_alumni(self.request.user)
        return context


class Home(BasePublicContext):
    template_name = "public/index.html"


class About(BasePublicContext):
    template_name = "public/about.html"


class Gallery(BasePublicContext):
    template_name = "public/gallery.html"


class Contact(BasePublicContext):
    template_name = "public/contact.html"
