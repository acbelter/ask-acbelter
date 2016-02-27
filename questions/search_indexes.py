from django.utils import timezone
from haystack import indexes

from questions.models import Question, Answer


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    search_text = indexes.CharField(document=True, use_template=True)
    # These fields are useful when you want to provide additional filtering options
    title = indexes.CharField(model_attr='title')
    question_text = indexes.CharField(model_attr='text')

    def get_model(self):
        return Question

    # This method prevent those future items from being indexed
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(creation_date__lte=timezone.now())


class AnswerIndex(indexes.SearchIndex, indexes.Indexable):
    search_text = indexes.CharField(document=True, use_template=True)
    # These fields are useful when you want to provide additional filtering options
    answer_text = indexes.CharField(model_attr='text')

    def get_model(self):
        return Answer

    # This method prevent those future items from being indexed
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(creation_date__lte=timezone.now())
