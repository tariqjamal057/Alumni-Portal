from django.db import models
from tinymce.models import HTMLField

from core.constant import YearChoices
from portal.models.base import BaseModel, PostUpVoteDownVote
from portal.models.college import Department
from portal.models.tags import Tag
from portal.models.user import User


class FinanceRequest(BaseModel, PostUpVoteDownVote):
    title = models.CharField(max_length=100)
    profile_img = models.ImageField(
        upload_to="student_images", null=True, blank=True, default="image/character.png"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="finance_request_student"
    )
    year = models.IntegerField(choices=YearChoices.choices)
    description = HTMLField()
    achievements = HTMLField(null=True, blank=True)
    other_performance = HTMLField(null=True, blank=True)
    comments = models.ManyToManyField(
        "FinanceRequestComment", related_name="finance_request_comments"
    )
    tags = models.ManyToManyField(Tag, related_name="finance_request_tags")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="finance_request_created_by"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="finance_request_updated_by",
    )


class FinanceRequestComment(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="finance_request_comment_user"
    )
    finance_request = models.ForeignKey(FinanceRequest, on_delete=models.CASCADE)
    text = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="finance_request_comment_created_by"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="finance_request_comment_updated_by",
    )


class FinanceRequestInterest(models.Model):
    post = models.ForeignKey(FinanceRequest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="finance_request_alumni")


class FinanceRequestInterestMessage(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="finance_request_alumni_message"
    )
    post_interest = models.ForeignKey(FinanceRequestInterest, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class FinanceRequestSponser(BaseModel):
    finance_request = models.ForeignKey(
        FinanceRequest, on_delete=models.CASCADE, related_name="finance_request"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alumni")
    amount = models.IntegerField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="finance_request_sponser_created_by"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="finance_request_sponser_updated_by",
    )
