from django.contrib.auth import get_user_model

from django.db import models
from tinymce import models as tinymce_models

from django.utils.timezone import now
from django.template.defaultfilters import slugify


class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Question(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.TextField(max_length=200)
    content = tinymce_models.HTMLField()
    timestamp = models.DateTimeField(default=now)
    tag = models.ManyToManyField(Tag)

    slug = models.SlugField(null=False, default="slug")

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def has_answer(self):
        return self.answers.all().count() > 0

    def is_active(self):
        return ((self.comments.all().count() > 0)
                or (True if self.answers.all().count() > 0 else False))

    @property
    def get_answers(self):
        return self.answers.all().order_by('-timestamp')

    @property
    def get_comments(self):
        return self.comments.all()


class QuestionComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(default=now)
    question = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.question.title + " | " + str(self.pk)


class Answer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = tinymce_models.HTMLField()
    timestamp = models.DateTimeField(default=now)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return self.question.title + " | answer: " + str(self.pk)

    @property
    def get_comments(self):
        return self.comments.all()


class AnswerComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(default=now)
    answer = models.ForeignKey(Answer, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return self.answer.question.title + " | answer: " + str(self.answer.pk) + " | comment: " + str(self.pk)











