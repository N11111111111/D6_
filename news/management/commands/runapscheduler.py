import logging
from datetime import datetime
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from news.models import *
import datetime



def my_job ():
    list_recipients = []
    for category in Category.objects.all():
        subject = f'Все статьи за неделю в категории {category}'
        date = datetime.datetime.now() - datetime.timedelta(days=7)
        posts = Post.objects.filter(category=category, dateCreation__gte= date)
        if posts.exists():
            for sub in category.subscribed.all():
                list_recipients.append(sub.email)
                html_content = render_to_string(
                    'send.html',
                    {
                        'username': sub,
                        'posts': posts,
                        'category': category,
                        'site': settings.SERVER_EMAIL,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=subject,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=list_recipients
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()


logger = logging.getLogger(__name__)


# функция, которая будет удалять неактуальные задачи

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
            day_of_week="mon", hour="08", minute="00"),
            id = "my_job",
            max_instances = 1,
            replace_existing = True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")