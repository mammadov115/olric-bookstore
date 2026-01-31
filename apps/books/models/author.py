from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)

    class Meta:
        app_label = 'books'

    def __str__(self):
        return self.name
