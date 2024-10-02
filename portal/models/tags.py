from django.db import models

from portal.models.base import BaseModel
from portal.models.user import User


class Tag(BaseModel):
    name = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tag_created_by")
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="tag_updated_by"
    )

    def __str__(self):
        return self.name

    def increment_count(self):
        self.count += 1
        self.save()

    def decrement_count(self):
        if self.count > 0:
            self.count -= 1
            self.save()

    @property
    def usage_count(self):
        return self.count
