from django.core.exceptions import ValidationError
from django.forms import forms, CharField, Textarea


class AddQuestionForm(forms.Form):
    title = CharField()
    text = CharField(widget=Textarea)
    tags = CharField(required=False)

    def clean_title(self):
        if len(self.cleaned_data['title']) > 200:
            raise ValidationError(u'Too long question title.')
        return self.cleaned_data['title']

    def clean_text(self):
        if len(self.cleaned_data['text']) > 1000:
            raise ValidationError(u'Too long question text.')
        return self.cleaned_data['text']

    def clean_tags(self):
        tags_list = self.cleaned_data['tags'].split(" ")
        if len(tags_list) > 10:
            raise ValidationError(u'Too much tags.')
        for tag in tags_list:
            if len(tag) > 16:
                raise ValidationError(u'Too long tag.')
        return self.cleaned_data['tags']


class AddAnswerForm(forms.Form):
    text = CharField(widget=Textarea)

    def clean_text(self):
        if len(self.cleaned_data['text']) > 1000:
            raise ValidationError(u'Too long answer text.')
        return self.cleaned_data['text']

