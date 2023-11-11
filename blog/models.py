from django.template.defaultfilters import slugify  # new

from tinymce import models as tinymce_models

from django.contrib.auth import get_user_model

from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import now


class Author(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
    
class Post(models.Model): 
    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = tinymce_models.HTMLField()
    thumbnail = models.ImageField()
    timestamp = models.DateTimeField(default=now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, default="slug") 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return redirect(reverse('post_detail', kwargs={
            'pk': self.pk,
            'slug': self.slug
        }))
    
    def save(self, *args, **kwargs):  #new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
