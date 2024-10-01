from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from portal.form import Help_Desk_Form
from portal.models import Post, PostResponse
from portal.utils import is_alumni
from portal.views.base import BasePublicContext


class AlumniDashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/alumni/index.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(posted_by=self.request.user)

        search_query = self.request.GET.get("s", "")
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )
            context["search_text"] = search_query

        posts = posts.order_by("-id")
        paginator = Paginator(posts, self.paginate_by)
        page_num = self.request.GET.get("page", 1)

        context.update(
            {
                "posts": paginator.get_page(page_num),
                "is_alumni": is_alumni(self.request.user),
                "form": Help_Desk_Form(),
                "search_query": search_query,
            }
        )
        return context


class CreateHelpDeskPost(LoginRequiredMixin, CreateView, BasePublicContext):
    template_name = "dashboard/alumni/help_desk_post/create_and_update.html"
    form_class = Help_Desk_Form
    success_url = reverse_lazy("dashboard.alumni")

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class UpdateHelpDeskPost(LoginRequiredMixin, UpdateView, BasePublicContext):
    model = Post
    form_class = Help_Desk_Form
    template_name = "dashboard/alumni/help_desk_post/create_and_update.html"
    success_url = reverse_lazy("dashboard.alumni")


class HelpDeskPostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "dashboard/alumni/help_desk_post/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs.get("pk"))
        interest = PostResponse.objects.filter(post=post).order_by("-id")
        context.update(
            {
                "alumni_interest": interest,
                "recent_intetest": interest[:5],
                "total_number_of_interest": interest.count(),
                "is_alumni": is_alumni(self.request.user),
            }
        )
        return context


class DeleteHelpDeskPostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = {"success": False, "msg_type": "error"}
        try:
            post = get_object_or_404(Post, id=kwargs.get("pk"), posted_by=request.user)
            post.delete()
            posts = Post.objects.filter(posted_by=request.user).order_by("-id")
            data.update(
                {
                    "html": render_to_string(
                        "dashboard/alumni/help_desk_post/list.html",
                        {"posts": posts},
                    ),
                    "success": True,
                    "msg": "Post Deleted Successfully.",
                    "msg_type": "success",
                }
            )
        except ObjectDoesNotExist:
            data["msg"] = "Post not found."
        except Exception:
            data["msg"] = "Unable to delete the post, please try again later."
        return JsonResponse(data)
