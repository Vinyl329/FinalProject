from celery import shared_task
from django.template.loader import render_to_string

from .models import Response, Subclass
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings


@shared_task
def response_send_email(response_id):
    response = Response.objects.get(id=response_id)
    send_mail(
        subject=f'Новый отклик на объявление!',
        message=f'{response.response_subclass.author}, ! На ваше объявление есть новый отклик!\n'
                f'Прочитать отклик:\nhttp://127.0.0.1:8000/myresponse/{response.response_subclass.id}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.response_subclass.author.email, ],
    )


@shared_task
def response_accept_send_email(response_subclass_id):
    response = Response.objects.get(id=response_subclass_id)
    send_mail(
        subject=f'Ваш отклик принят!',
        message=f'{response.author}, aвтор объявления {response.response_subclass.title} принял Ваш отклик!\n'
                f'Посмотреть принятые отклики:\nhttp://127.0.0.1:8000/myresponse',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.response_subclass.author.email, ],
    )