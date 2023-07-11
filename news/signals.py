from django.template.loader import render_to_string
from .models import *
from django.db.models.signals import *
from django.dispatch import receiver
from django.core.mail import send_mail
import datetime
from django.conf import settings



dict_message = dict()


@receiver(post_save, sender=Post)
def notify_managers_post(sender, instance, created, **kwargs):
    for category in instance.category.all():
        recipients = [user.email for user in category.subscribed.all()]
        if created:
            start_word = 'Новая'
        else:
            start_word = 'Обновлена'
        subject=f'На сайте NewsPaper {start_word.lower()} статья: {instance.title}'
        message=f'NewsPaper.\n{instance.title}:\n{instance.text[:50]}...\nПодробнее: http://127.0.0.1:8000/news/news/{instance.id}'
        from_email=settings.SERVER_EMAIL

        send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipients,
                fail_silently=False
            )


@receiver(m2m_changed, sender=Post.category.through)
def notify_managers_posts(instance, action, pk_set, *args, **kwargs):
    if action == 'post_add':
        html_content = render_to_string(
            'post_create.html',
            {'post': instance, }
        )
        for pk in pk_set:
            category = Category.objects.get(pk=pk)
            recipients = [user.email for user in category.subscribed.all()]
            subject=f'На сайте NewsPaper новая статья: {instance.title}'
            message=f'NewsPaper.\n{instance.title}:\n{instance.text[:30]}...\nПодробнее: http://127.0.0.1:8000/news/news/{instance.id}'
            from_email=settings.SERVER_EMAIL
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipients,
                fail_silently=False
            )

