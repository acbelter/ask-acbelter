from django.contrib import admin

# Register your models here.
from questions.models import *


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'creation_date', 'rating', 'answers_count')


class QuestionRatingAdmin(admin.ModelAdmin):
    list_display = ('member', 'question', 'rating_delta')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'question', 'correct_answer', 'creation_date', 'rating')


class AnswerRatingAdmin(admin.ModelAdmin):
    list_display = ('member', 'answer', 'rating_delta')


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionRating, QuestionRatingAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(AnswerRating, AnswerRatingAdmin)
