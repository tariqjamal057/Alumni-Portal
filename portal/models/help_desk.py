from django.db import models
from tinymce.models import HTMLField

from portal.models.base import BaseModel, PostUpVoteDownVote
from portal.models.tags import Tag
from portal.models.user import User


class PostType(BaseModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=1, unique=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_type_created_by"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="post_type_updated_by"
    )

    def __str__(self):
        return self.name


class HelpDesk(BaseModel, PostUpVoteDownVote):
    title = models.CharField(max_length=200)
    content = HTMLField()
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    comments = models.ManyToManyField("HelpDeskComment", related_name="help_desk_comments")
    tags = models.ManyToManyField(Tag, related_name="help_desk_tags")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="help_desk_created_by"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="help_desk_updated_by"
    )


class HelpDeskComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="help_desk_comment_user")
    help_desk = models.ForeignKey(HelpDesk, on_delete=models.CASCADE)
    text = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="help_desk_comment_created_by"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="help_desk_comment_updated_by",
    )


class HelpDeskInterest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="help_desk_interest_user"
    )
    post = models.ForeignKey(HelpDesk, on_delete=models.CASCADE)


class HelpDeskInterestMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="help_desk_user_message")
    post_interest = models.ForeignKey(HelpDeskInterest, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
