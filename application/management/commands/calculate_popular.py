import random
import operator

from django.core.management import BaseCommand

from application import cron_cache
from questions.models import *

popular_tags_count = 5
popular_members_count = 5


def update_ratings():
    print "Start updating ratings..."
    for question in Question.objects.all():
        question.rating = random_rating()
        question.save()
    for answer in Answer.objects.all():
        answer.rating = random_rating()
        answer.save()


def random_rating():
    return random.randint(0, 1000)


def calculate_popular_tags():
    print "Start calculating popular tags at time " + str(timezone.now())
    tags_count_dict = {}
    for question in Question.objects.all():
        for tag in question.tags.all():
            tags_count_dict[tag] = tags_count_dict.get(tag, 0) + 1

    # Sort dictionary by values and get first n items
    popular_tags = sorted(tags_count_dict.items(), key=operator.itemgetter(1), reverse=True)[:popular_tags_count]

    print popular_tags

    cron_cache.set_popular_tags([x[0] for x in popular_tags])


def calculate_best_members():
    print "Start calculating best members at time " + str(timezone.now())
    member_answers_rating_dict = {}
    for answer in Answer.objects.all():
        member_answers_rating_dict[answer.author] = member_answers_rating_dict.get(answer.author, 0) + answer.rating

    # Sort dictionary by values and get first n items
    best_members = sorted(member_answers_rating_dict.items(), key=operator.itemgetter(1), reverse=True)[:popular_members_count]

    print (best_members)

    cron_cache.set_best_members([x[0] for x in best_members])


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        update_ratings()
        calculate_popular_tags()
        calculate_best_members()
