from django.db import models
from django.contrib.auth.models import User


class ImageUpload(models.Model):
    img_id=models.CharField(max_length=255)
    img = models.ImageField(upload_to='testing_image/', null=True, blank=True)

    def __str__(self):
        return self.img_id
