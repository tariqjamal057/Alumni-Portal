from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView

from portal.form import Help_Desk_Form
from portal.models import Post, PostResponse
from portal.utils import is_alumni


class AlumniDashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/alumni/index.html"
    paginate_by = 10
    form = Help_Desk_Form()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(posted_by=self.request.user).order_by("-id")
        page_num = self.request.GET.get("page", 1)
        paginator = Paginator(posts, self.paginate_by)
        context.update(
            {
                "posts": paginator.get_page(page_num),
                "is_alumini": is_alumni(self.request.user),
                "form": self.form,
            }
        )
        return context


class CreateHelpDeskPost(LoginRequiredMixin, CreateView):
    template_name = "dashboard/alumni/help_desk_post/create_and_update.html"
    form_class = Help_Desk_Form
    success_url = reverse_lazy("dashboard.alumni")

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class UpdateHelpDeskPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = Help_Desk_Form
    template_name = "dashboard/alumni/help_desk_post/create_and_update.html"
    success_url = reverse_lazy("dashboard.alumni")


class HelpDeskPostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "dashboard/alumni/help_desk_post/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        interest = PostResponse.objects.filter(post=post).order_by("-id")
        recent_interest = interest[:5]
        context.update(
            {
                "alumni_interest": interest,
                "recent_intetest": recent_interest,
                "total_number_of_interest": len(interest),
                "is_alumini": is_alumni(self.request.user),
            }
        )
        return context


@method_decorator(csrf_exempt, name="dispatch")
class DeleteHelpDeskPostView(View):
    def post(self, request, *args, **kwargs):
        data = dict()
        id = request.POST.get("id")
        try:
            financial_request = Post.objects.filter(id=id)
            financial_request.delete()
            posts = Post.objects.filter(posted_by=request.user)
            data["html"] = render_to_string(
                "dashboard/alumni/help_desk_post/list.html",
                {
                    "posts": posts,
                },
            )
            data["success"] = True
        except Exception as e:
            data["success"] = False
        return JsonResponse(data)
