from django.conf.urls import url

import questions.views

urlpatterns = [
    url(r'^$', questions.views.new_questions, name="start-questions"),
    url(r'^ask/$', questions.views.ask_question, name="ask-question"),
    url(r'^new_questions/$', questions.views.new_questions, name="new-questions"),
    url(r'^popular_questions/$', questions.views.popular_questions, name="popular-questions"),
    url(r'^question/(?P<question_id>\d+)/$', questions.views.question_answers, name="answers"),
    url(r'^tag/(?P<tag_value>\w+)$', questions.views.tagged_questions, name="tagged-questions"),
    url(r'^like_question/$', questions.views.like_question, name='like-question'),
    url(r'^dislike_question/$', questions.views.dislike_question, name='dislike-question'),
    url(r'^like_answer/$', questions.views.like_answer, name='like-answer'),
    url(r'^dislike_answer/$', questions.views.dislike_answer, name='dislike-answer'),
    url(r'^check_correct_answer/$', questions.views.check_correct_answer, name='check-correct-answer'),
]
