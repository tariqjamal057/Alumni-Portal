from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from portal.form import Help_Desk_Form
from portal.models import (
    HelpDesk,
    HelpDeskComment,
    HelpDeskInterest,
    HelpDeskInterestMessage,
)
from portal.models.help_desk import PostType
from portal.models.user import User


class AlumniDashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/alumni/index.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = HelpDesk.objects.filter(created_by=self.request.user).annotate(
            comment_count=Count("comments", distinct=True),
            upvote_count=Count("upvotes", distinct=True),
            downvote_count=Count("downvotes", distinct=True),
        )

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
                "form": Help_Desk_Form(),
                "search_query": search_query,
            }
        )
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    template_name = "dashboard/alumni/help_desk_post/create_and_update.html"
    form_class = Help_Desk_Form
    success_url = reverse_lazy("dashboard.alumni")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = HelpDesk
    form_class = Help_Desk_Form
    template_name = "dashboard/alumni/help_desk_post/create_and_update.html"
    success_url = reverse_lazy("dashboard.alumni")
    pk_url_kwarg = "post_id"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PostDetail(LoginRequiredMixin, DetailView):
    model = HelpDesk
    template_name = "dashboard/alumni/help_desk_post/detail.html"
    pk_url_kwarg = "post_id"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.annotate(
            comment_count=Count("comments", distinct=True),
            upvote_count=Count("upvotes", distinct=True),
            downvote_count=Count("downvotes", distinct=True),
        )

        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_interests = HelpDeskInterest.objects.filter(post=context["object"]).order_by("-id")[
            :5
        ]
        comments = HelpDeskComment.objects.filter(help_desk=context["object"]).order_by("-id")
        context.update({"post_interests": post_interests, "comments": comments})
        return context


class DeletePost(LoginRequiredMixin, View):
    pk_url_kwarg = "post_id"

    def post(self, request, *args, **kwargs):
        data = {"success": False, "msg_type": "error"}
        try:
            post = get_object_or_404(HelpDesk, id=kwargs.get("post_id"), created_by=request.user)
            post.delete()
            posts = (
                HelpDesk.objects.filter(created_by=request.user)
                .annotate(
                    comment_count=Count("comments"),
                    upvote_count=Count("upvotes"),
                    downvote_count=Count("downvotes"),
                )
                .order_by("-id")
            )
            print(posts)
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


class UserChat(LoginRequiredMixin, View):
    template_name = "dashboard/alumni/help_desk_post/chat/index.html"

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(HelpDesk, id=kwargs.get("post_id"), created_by=request.user)
        post_interests = HelpDeskInterest.objects.filter(post=post)
        return render(
            request, self.template_name, {"post_interests": post_interests, "post": post}
        )


class GetMessage(LoginRequiredMixin, View):
    template_name = "dashboard/alumni/help_desk_post/chat/message_container.html"

    def post(self, request, *args, **kwargs):
        post_interest = get_object_or_404(
            HelpDeskInterest, post_id=kwargs.get("post_id"), user_id=request.POST.get("user_id")
        )
        post_messages = HelpDeskInterestMessage.objects.filter(post_interest=post_interest)
        return JsonResponse(
            {
                "html": render_to_string(
                    self.template_name,
                    {
                        "post_interest": post_interest,
                        "messages": post_messages,
                        "request": request,
                    },
                )
            }
        )


class AddMessage(LoginRequiredMixin, View):
    template_name = "dashboard/alumni/help_desk_post/chat/message.html"

    def post(self, request, *args, **kwargs):
        post_interest = get_object_or_404(
            HelpDeskInterest, id=request.POST.get("post_interest_id")
        )
        HelpDeskInterestMessage.objects.create(
            post_interest=post_interest,
            user_id=request.user.id,
            message=request.POST.get("message"),
        )
        post_messages = HelpDeskInterestMessage.objects.filter(post_interest=post_interest)
        return JsonResponse(
            {
                "html": render_to_string(
                    self.template_name, {"messages": post_messages, "request": request}
                )
            }
        )


class RefreshMessage(LoginRequiredMixin, View):
    template_name = "dashboard/alumni/help_desk_post/chat/message.html"

    def post(self, request, *args, **kwargs):
        post_interest = get_object_or_404(
            HelpDeskInterest, id=request.POST.get("post_interest_id")
        )
        post_messages = HelpDeskInterestMessage.objects.filter(post_interest=post_interest)
        return JsonResponse(
            {
                "html": render_to_string(
                    self.template_name, {"messages": post_messages, "request": request}
                )
            }
        )


class AddComment(LoginRequiredMixin, View):
    template_name = "dashboard/alumni/help_desk_post/comment.html"

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(HelpDesk, id=kwargs.get("post_id"))
        user = get_object_or_404(User, id=request.user.id)
        post_comment = HelpDeskComment.objects.create(
            help_desk=post, user=user, text=request.POST.get("text"), created_by=request.user
        )
        post.comments.add(post_comment)
        comments = HelpDeskComment.objects.filter(help_desk=post).order_by("-id")
        return JsonResponse(
            {
                "html": render_to_string(
                    self.template_name, {"comments": comments, "request": request}
                )
            }
        )


class Addvote(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(HelpDesk, id=kwargs.get("post_id"))
        vote_type = kwargs.get("vote_type")
        # Remove user from the opposite vote type
        opposite_vote_type = "upvotes" if vote_type == "downvotes" else "downvotes"
        getattr(post, opposite_vote_type).remove(request.user)
        # Add user to the requested vote type
        getattr(post, vote_type).add(request.user)
        return JsonResponse({"success": True})
