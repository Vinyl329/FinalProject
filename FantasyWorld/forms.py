from django import forms
from .models import Subclass, Response
from ckeditor.fields import RichTextFormField
from allauth.account.forms import SignupForm
from string import hexdigits
import random
from django.conf import settings
from django.core.mail import send_mail


class SubclassForm(forms.ModelForm):

    class Meta:
        model = Subclass
        fields = ['category', 'title', 'text']
        widgets = {
            'text': RichTextFormField(),
        }


    def __init__(self, *args, **kwargs):
        super(SubclassForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Категория:"
        self.fields['title'].label = "Заголовок:"
        self.fields['text'].label = "Текст объявления:"



class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text_response']

    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        self.fields['text_response'].label = "Текст отклика:"

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = '' .join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user