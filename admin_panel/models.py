from django.db import models

# Create your models here.


class Banner(models.Model):
    caption = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='banner_images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.caption