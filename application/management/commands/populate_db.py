# encoding: utf-8
import random

from django.contrib.auth import hashers
from django.core.management import BaseCommand


# Пользователи > 10 000
# Вопросы > 100 000
# Ответы > 1 000 000
# Тэги > 10 000
# Оценки пользователей > 2 000 000

# Очистка базы данных: python manage.py flush
# Заполнение базы данных: python manage.py populate_db
from questions.models import *


all_tags_count = 10
question_tags_count = 1
members_count = 5
member_questions_count = 5
question_answers_count = 5


def populate():
    tags = populate_tags()
    print "Start populating members..."
    members = []
    for i in range(0, members_count):
        username = "user" + str(i)
        email = "user" + str(i) + "@mail.ru"
        password = hashers.make_password(str(i))
        nick = "nick" + str(i)
        avatar = "avatar" + str(random.getrandbits(1)) + ".png"
        rating = 0
        member = Member(username=username, email=email,
                        password=password, nick=nick,
                        avatar=avatar, rating=rating)
        members.append(member)
        member.save()
        add_questions(member, tags)
        print "Added member " + member.nick
    populate_answers(members)
    populate_ratings(members)


def random_rating():
    return random.randint(0, 1000)


def add_questions(member, all_tags):
    print "Adding questions to member " + member.nick
    for i in range(0, member_questions_count):
        title = "Question " + str(i) + " from " + member.nick
        text = "Question text"
        creation_date = timezone.now().replace(day=random.randint(1, 28))
        tags = random.sample(all_tags, question_tags_count)

        rating = random_rating()

        question = Question(title=title, text=text, author=member,
                            creation_date=creation_date, rating=rating,
                            answers_count=question_answers_count)
        question.save()
        question.tags.add(*tags)
        question.save()


def populate_answers(all_members):
    print "Start populating answers..."
    answers = []
    for question in Question.objects.all():
        random_members = random.sample(all_members, question_answers_count)

        for member in random_members:
            text = "Answer text from member " + member.nick
            correct_answer = bool(random.getrandbits(1))
            creation_date = timezone.now().replace(day=random.randint(1, 28))
            rating = random_rating()

            answer = Answer(text=text, author=member, question=question,
                            correct_answer=correct_answer, creation_date=creation_date,
                            rating=rating)
            answers.append(answer)
    Answer.objects.bulk_create(answers)


def populate_tags():
    print "Start populating tags..."
    tags = []
    for i in range(0, all_tags_count):
        value = "tag" + str(i)
        tag = Tag(value=value)
        tag.save()
        tags.append(tag)
    # Tag.objects.bulk_create(tags) doesn't send signals!
    return tags


def populate_ratings(all_members):
    print "Start populating ratings..."
    qratings = []
    aratings = []
    for member in all_members:
        random_questions = Question.objects.all().order_by('?')[:10]
        random_answers = Answer.objects.all().order_by('?')[:10]

        for question in random_questions:
            rating_delta = 1 if bool(random.getrandbits(1)) else -1
            question_rating = QuestionRating(member=member, question=question, rating_delta=rating_delta)
            qratings.append(question_rating)

        for answer in random_answers:
            rating_delta = 1 if bool(random.getrandbits(1)) else -1
            answer_rating = AnswerRating(member=member, answer=answer, rating_delta=rating_delta)
            aratings.append(answer_rating)
    QuestionRating.objects.bulk_create(qratings)
    AnswerRating.objects.bulk_create(aratings)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        dt1 = timezone.now()
        populate()
        dt2 = timezone.now() - dt1
        print "Populating time " + str(dt2)
        print "Tags count: %d" % Tag.objects.all().count()
        print "Members count: %d" % Member.objects.all().count()
        print "Questions count: %d" % Question.objects.all().count()
        print "Question ratings count: %d" % QuestionRating.objects.all().count()
        print "Answers count: %d" % Answer.objects.all().count()
        print "Answer ratings count: %d" % AnswerRating.objects.all().count()
