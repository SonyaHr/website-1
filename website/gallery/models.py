from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to="photos")
    description = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.description if self.description else "No description"
