from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def notify_managers_posts(sender, instance, created, **kwargs):
    if created:
        title = f' Пользователь {instance.username} ! Вы зарегистрированы на сайте NewsPaper.'
        message = f'Добрый день, {instance.username}!\n' \
                  f'Благодарим вас за регистрацию на сайте NewsPaper.\n' \
                  f'Перейти в личный кабинет на сайте NewsPaper: http://127.0.0.1:8000\n' \
                  f'где сможете стать автором, подписаться на понравившиеся статьи и новости.'
        send_mail(
            subject=title,
            message=message,
            from_email=settings.SERVER_EMAIL,
            recipient_list=[instance.email,]
            )