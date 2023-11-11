from django.db import models

from blog.models import Author
from django.utils.timezone import now
from django.template.defaultfilters import slugify 



# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
    

class Course(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    url = models.CharField(max_length=150, default="https://www.youtube.com/@iut_AcademicHelp")
    thumbnail = models.ImageField()
    timestamp = models.DateTimeField(default=now)
    slug = models.SlugField(null=False, default="slug")

    def save(self, *args, **kwargs):  
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
