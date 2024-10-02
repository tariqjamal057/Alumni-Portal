from django.db import models

from portal.models.base import BaseModel
from portal.models.user import User


class GaleryCategory(BaseModel):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="gallery_created_by"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="gallery_updated_by"
    )

    def __str__(self):
        return self.name


class GalleryImage(BaseModel):
    category = models.ForeignKey(GaleryCategory, on_delete=models.CASCADE, related_name="images")
    images = models.ManyToManyField("Image", related_name="galleries")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="gallery_images_created_by"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="gallery_images_updated_by",
    )

    def __str__(self):
        return f"Gallery for {self.category.name}"


class Image(models.Model):
    image = models.ImageField(upload_to="gallery_images/")
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
