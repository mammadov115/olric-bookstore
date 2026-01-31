from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='publishers/', blank=True)

    class Meta:
        app_label = 'books'

    def __str__(self):
        return self.name
