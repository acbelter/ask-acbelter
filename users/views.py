from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from application import cron_cache
from users.forms import RegistrationForm
from users.models import Member


# Create your views here.
def register(request):
    form = RegistrationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data['login']
        password = form.cleaned_data['password']

        member = Member.objects.create_user(username=username,
                                            email=form.cleaned_data['email'],
                                            password=password)
        member.nick = form.cleaned_data['nick']
        member.avatar = form.cleaned_data['avatar']
        member.save()

        new_member = authenticate(username=username,
                                  password=password)
        login(request, new_member)

        return redirect('questions.views.new_questions')
    return render(request, 'registration/registration.html', {
        'popular_tags': cron_cache.get_popular_tags(),
        'best_members': cron_cache.get_best_members(),
        'form': form,
    })


@login_required
def settings(request):
    return HttpResponseNotFound('<h1>Not implemented</h1>')


@login_required
def user_details(request, user_id):
    return HttpResponseNotFound('<h1>Not implemented</h1>')
