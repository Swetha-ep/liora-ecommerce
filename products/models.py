from django.db import models
from django.utils.text import slugify

# Create your models here.

class Categories(models.Model):
    name = models.CharField( max_length=50,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    image = models.ImageField(upload_to='category_images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
