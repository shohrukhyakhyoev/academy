from django.contrib import admin
from community.models import Tag, Question, QuestionComment, Answer, AnswerComment

# Register your models here.
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(QuestionComment)
admin.site.register(Answer)
admin.site.register(AnswerComment)