from django.db import models


class BaseModel(models.Model):
    """Base model for all models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostUpVoteDownVote:
    upvotes = models.ManyToManyField("User", related_name="post_upvotes", blank=True)
    downvotes = models.ManyToManyField("User", related_name="post_downvotes", blank=True)

    def upvote(self, user):
        if user in self.downvotes.all():
            self.downvotes.remove(user)
        self.upvotes.add(user)

    def downvote(self, user):
        if user in self.upvotes.all():
            self.upvotes.remove(user)
        self.downvotes.add(user)
