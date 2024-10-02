from django.db import models
from tinymce.models import HTMLField

from portal.models.base import BaseModel, PostUpVoteDownVote
from portal.models.tags import Tag
from portal.models.user import User


class TechHelpPost(BaseModel, PostUpVoteDownVote):
    title = models.CharField(max_length=200)
    stack = models.CharField(max_length=100)
    content = HTMLField()
    comments = models.ManyToManyField(
        "TechHelpPostComment", related_name="tech_help_post_comments"
    )
    tags = models.ManyToManyField(Tag, related_name="tech_help_post_tags")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tech_help_created_by"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="tech_help_updated_by"
    )


class TechHelpPostComment(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tech_help_post_comment_user"
    )
    tech_help_post = models.ForeignKey(TechHelpPost, on_delete=models.CASCADE)
    text = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tech_help_comment_created_by"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tech_help_comment_updated_by",
    )


class TechHelpPostInterest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tech_help_post_interest_user"
    )
    post = models.ForeignKey(TechHelpPost, on_delete=models.CASCADE)


class TechHelpPostInterestMessage(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tech_help_post_user_message"
    )
    post_interest = models.ForeignKey(TechHelpPostInterest, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
