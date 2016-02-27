from django.db import models

# Create your models here.
from django.utils import timezone
from tags.models import Tag
from users.models import Member


class QuestionQuerySet(models.QuerySet):
    def new_questions(self):
        return self.order_by('creation_date')

    def popular_questions(self):
        return self.filter(rating__gt=500).order_by('rating').reverse()

    def question_by_tag(self, tag_value):
        tag = Tag.objects.all().filter(value=tag_value)
        return self.filter(tags__in=tag)

    def question_by_id(self, question_id):
        return self.get(id=question_id)


class AnswerQuerySet(models.QuerySet):
    def answers_by_question(self, question):
        return self.filter(question=question).order_by('rating').reverse()

    def answer_by_id(self, answer_id):
        return self.get(id=answer_id)


class Question(models.Model):
    title = models.CharField(u'title', max_length=255)
    text = models.TextField(u'text')
    author = models.ForeignKey(Member)
    creation_date = models.DateTimeField(u'creation date', default=timezone.now, blank=True)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(u'rating', default=0)
    answers_count = models.PositiveIntegerField(u'answers count', default=0)
    objects = QuestionQuerySet.as_manager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-creation_date']


class QuestionRating(models.Model):
    member = models.ForeignKey(Member)
    question = models.ForeignKey(Question)
    # rating_delta is 1 or -1
    rating_delta = models.SmallIntegerField()


class Answer(models.Model):
    text = models.TextField(u'text')
    author = models.ForeignKey(Member)
    question = models.ForeignKey(Question)
    correct_answer = models.BooleanField(u'correct answer', default=False)
    creation_date = models.DateTimeField(u'creation date', default=timezone.now, blank=True)
    rating = models.IntegerField(u'rating', default=0)
    objects = AnswerQuerySet().as_manager()

    def __unicode__(self):
        return self.text


class AnswerRating(models.Model):
    member = models.ForeignKey(Member)
    answer = models.ForeignKey(Answer)
    # rating_delta is 1 or -1
    rating_delta = models.SmallIntegerField()
