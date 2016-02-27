from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from application import cron_cache
from questions.forms import AddQuestionForm, AddAnswerForm
from questions.models import *

page_items = 5


# Create your views here.
def tagged_questions(request, tag_value):
    all_questions = Question.objects.question_by_tag(tag_value)
    paginator = Paginator(all_questions, page_items)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'popular_tags': cron_cache.get_popular_tags(),
        'best_members': cron_cache.get_best_members(),
        'filter_tag_value': tag_value,
        'questions': questions,
    })


@login_required
def ask_question(request):
    form = AddQuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        new_question = Question(title=form.cleaned_data['title'],
                                text=form.cleaned_data['text'])
        new_question.author = request.user
        new_question.save()

        tags_list = form.cleaned_data['tags'].split(" ")
        tags = []
        for tag_value in tags_list:
            t = Tag.objects.get_or_create(value=tag_value)
            tags.append(t)

        for (key, value) in tags:
            new_question.tags.add(key)
        new_question.save()
        return redirect('questions.views.question_answers', question_id=new_question.id)
    return render(request, 'ask.html', {
        'popular_tags': cron_cache.get_popular_tags(),
        'best_members': cron_cache.get_best_members(),
        'form': form,
    })


def new_questions(request):
    all_questions = Question.objects.new_questions()

    paginator = Paginator(all_questions, page_items)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'popular_tags': cron_cache.get_popular_tags(),
        'best_members': cron_cache.get_best_members(),
        'questions': questions,
    })


def popular_questions(request):
    all_questions = Question.objects.popular_questions()

    paginator = Paginator(all_questions, page_items)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'popular_tags': cron_cache.get_popular_tags(),
        'best_members': cron_cache.get_best_members(),
        'questions': questions,
    })


def question_answers(request, question_id):
    question = Question.objects.question_by_id(question_id)
    answers = Answer.objects.answers_by_question(question)

    form = AddAnswerForm(request.POST or None)
    if request.method == "POST" and form.is_valid() and request.user.is_authenticated():
        new_answer = Answer(text=form.cleaned_data['text'])
        new_answer.question = question
        new_answer.author = request.user
        new_answer.save()

        question.answers_count += 1
        question.save()

        # Send email to question author
        subject = 'New answer for \"' + question.title + '\"'
        message = str(request.build_absolute_uri()) + '#' + str(new_answer.id)
        from_email = settings.EMAIL_HOST_USER
        to_email = str(question.author.email)
        send_mail(subject, message, from_email, [to_email], fail_silently=settings.DEBUG)

        return redirect(reverse('questions.views.question_answers',
                                kwargs={'question_id': question_id}) + '#' + str(new_answer.id))
    return render(request, 'question.html', {
        'popular_tags': cron_cache.get_popular_tags(),
        'best_members': cron_cache.get_best_members(),
        'question': question,
        'answers': answers,
        'form': form,
    })


def like_question(request):
    return rate_question(request, rating_delta=1)


def dislike_question(request):
    return rate_question(request, rating_delta=-1)


def rate_question(request, rating_delta):
    if not request.user.is_authenticated():
        data = {
            'status': 'error',
            'message': 'You are not logged in.'
        }
        return JsonResponse(data)
    if request.method == "POST":
        question_id = request.POST['question_id']
        question = Question.objects.question_by_id(question_id)

        if question.author == request.user:
            data = {
                'status': 'error',
                'message': 'You can\'t rate your own question.'
            }
            return JsonResponse(data)

        if QuestionRating.objects.filter(member=request.user, question__id=question_id).exists():
            data = {
                'status': 'error',
                'message': 'You are already rate this question.'
            }
            return JsonResponse(data)

        question_rating = QuestionRating(rating_delta=rating_delta)
        question_rating.member = request.user
        question_rating.question = question
        question_rating.save()

        question.rating += rating_delta
        question.save()

        data = {
            'status': 'ok',
            'rating': question.rating,
            'message': 'Question is successfully rated.'
        }
        return JsonResponse(data)


def like_answer(request):
    return rate_answer(request, rating_delta=1)


def dislike_answer(request):
    return rate_answer(request, rating_delta=-1)


def rate_answer(request, rating_delta):
    if not request.user.is_authenticated():
        data = {
            'status': 'error',
            'message': 'You are not logged in.'
        }
        return JsonResponse(data)
    if request.method == "POST":
        answer_id = request.POST['answer_id']
        answer = Answer.objects.answer_by_id(answer_id)

        if answer.author == request.user:
            data = {
                'status': 'error',
                'message': 'You can\'t rate your own answer.'
            }
            return JsonResponse(data)

        if AnswerRating.objects.filter(member=request.user, answer__id=answer_id).exists():
            data = {
                'status': 'error',
                'message': 'You are already rate this answer.'
            }
            return JsonResponse(data)

        answer_rating = AnswerRating(rating_delta=rating_delta)
        answer_rating.member = request.user
        answer_rating.answer = answer
        answer_rating.save()

        answer.rating += rating_delta
        answer.save()

        data = {
            'status': 'ok',
            'rating': answer.rating,
            'message': 'Answer is successfully rated.'
        }
        return JsonResponse(data)


def check_correct_answer(request):
    # "true" or "false"
    checked = request.POST['checked']
    if not request.user.is_authenticated():
        data = {
            'status': 'error',
            'checked': checked,
            'message': 'You are not logged in.'
        }
        return JsonResponse(data)

    if request.method == "POST":
        answer_id = request.POST['answer_id']
        checked = request.POST['checked']
        answer = Answer.objects.answer_by_id(answer_id)

        if not answer.question.author == request.user:
            data = {
                'status': 'error',
                'checked': checked,
                'message': 'This question isn\'t yours.'
            }
            return JsonResponse(data)

        if checked == "true":
            answer.correct_answer = False
            answer.save()

            data = {
                'status': 'ok',
                'checked': 'false',
                'message': 'Answer is successfully unchecked.'
            }
            return JsonResponse(data)
        else:
            answer.correct_answer = True
            answer.save()

            data = {
                'status': 'ok',
                'checked': 'true',
                'message': 'Answer is successfully checked.'
            }
            return JsonResponse(data)
