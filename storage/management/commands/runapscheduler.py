import datetime
import logging
import re
from textwrap import dedent

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand
from django.utils.timezone import localdate
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from storage.models import Order

logger = logging.getLogger(__name__)


def get_orders_to_dates(dates):
    return Order.objects.filter(box__is_available=False, end_order__in=dates)\
        .values(
        'id',
        'customer__first_name',
        'customer__email',
        'end_order',
        'box__number',
        'box__storage__description',
        'box__storage__address',
    )


@util.close_old_connections
def inform_about_overdue_rent():
    max_storage_term = 6
    now = localdate()
    dates_catalog = {}
    dates = []
    for months_number in range(1, 7):
        search_date = now - relativedelta(months=months_number)
        dates.append(search_date)
        deadline = search_date + relativedelta(months=max_storage_term)
        dates_catalog[search_date] = {
            'months_number': months_number,
            'deadline': deadline,
        }

    orders = get_orders_to_dates(dates)

    message_template = '''\
    Здравствуйте, {name}!

    Cрок аренды завершился {months_number} мес. назад ({ends_at}) :
    заказ № {order_id}
    cклад {storage_descr}, по адресу {storage_address}
    бокс № {box_number}.

    Заберите, пожалуйста, вещи.
    Сейчас они хранятся из расчета повышенного тарифа.
    Если Вы не заберете вещи до {deadline}, они будут утилизированы.

    -----------
    С уважением, администрация SelfStorage
    '''

    messages = []
    for order in orders:
        ends_at = order['end_order']
        date_card = dates_catalog[ends_at]
        date_format = '%d.%m.%Y'
        months_number = date_card['months_number']

        message_text = message_template.format(
            name=order['customer__first_name'],
            order_id=order['id'],
            storage_descr=order['box__storage__description'],
            storage_address=order['box__storage__address'],
            box_number=order['box__number'],
            ends_at=ends_at.strftime(date_format),
            months_number=months_number,
            deadline=date_card['deadline'].strftime(date_format),
        )

        message = (
            f'cрок аренды истек {months_number} мес. назад',
            dedent(message_text),
            None,
            [order['customer__email']]
        )

        messages.append(message)

    if not messages:
        return

    send_mass_mail(datatuple=messages)


@util.close_old_connections
def inform_about_last_rent_day():
    now = localdate()
    orders = get_orders_to_dates([now])
    message_template = '''\
    Здравствуйте, {name}!

    Сегодня, {ends_at}, завершается срок аренды:
    заказ № {order_id}
    cклад {storage_descr}, по адресу {storage_address}
    бокс № {box_number}.

    Заберите, пожалуйста, вещи.
    С завтрашнего дня хранение вещей будет происходить\
    по повышенному тарифу.
    Если Вы не заберете вещи в течение 6 месяцев, они будут утилизированы.

    -----------
    С уважением, администрация SelfStorage
    '''
    messages = []
    for order in orders:
        ends_at = order['end_order'].strftime('%d.%m.%Y')

        message_text = message_template.format(
            name=order['customer__first_name'],
            order_id=order['id'],
            storage_descr=order['box__storage__description'],
            storage_address=order['box__storage__address'],
            box_number=order['box__number'],
            ends_at=ends_at,
        )
        message_text = re.sub(' +', ' ', message_text)
        message = (
            'Срок аренды завершен',
            dedent(message_text),
            None,
            [order['customer__email']]
        )

        messages.append(message)

    if not messages:
        return

    send_mass_mail(datatuple=messages)


@util.close_old_connections
def inform_about_rent_end():
    now = localdate()
    in_3_days = now + datetime.timedelta(days=3)
    in_1_week = now + datetime.timedelta(days=7)
    in_2_weeks = now + datetime.timedelta(days=14)
    in_1_month = now + relativedelta(months=1)

    orders = get_orders_to_dates(
        [
            in_3_days,
            in_1_week,
            in_2_weeks,
            in_1_month,
        ]
    )

    message_template = '''\n
    Здравствуйте, {name}!

    Через {in_phrase} ({ends_at}) завершается срок аренды:
    заказ № {order_id}
    cклад {storage_descr}, по адресу {storage_address}
    бокс № {box_number}.

    Не забудьте забрать вещи.

    -----------
    С уважением, администрация SelfStorage
    '''

    messages = []
    for order in orders:
        if order['end_order'] == in_3_days:
            in_phrase = '3 дня'
        elif order['end_order'] == in_1_week:
            in_phrase = 'неделю'
        elif order['end_order'] == in_2_weeks:
            in_phrase = 'две недели'
        else:
            in_phrase = 'месяц'

        ends_at = order['end_order'].strftime('%d.%m.%Y')

        message_text = message_template.format(
            name=order['customer__first_name'],
            in_phrase=in_phrase,
            order_id=order['id'],
            storage_descr=order['box__storage__description'],
            storage_address=order['box__storage__address'],
            box_number=order['box__number'],
            ends_at=ends_at,
        )
        message = (
            'Скоро завершается срок аренды бокса',
            dedent(message_text),
            None,
            [order['customer__email']]
        )

        messages.append(message)

    if not messages:
        return

    send_mass_mail(datatuple=messages)

# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical job
    execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            inform_about_rent_end,
            trigger=CronTrigger(
                minute=f"*/{settings.NOTIFICATION_MAILING_INTERVAL_MINUTES}"
            ),
            # The `id` assigned to each job MUST be unique
            id="Inform about rent end",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'inform_about_rent_end'.")

        scheduler.add_job(
            inform_about_last_rent_day,
            trigger=CronTrigger(
                minute=f"*/{settings.NOTIFICATION_MAILING_INTERVAL_MINUTES}"
            ),
            # The `id` assigned to each job MUST be unique
            id="Inform about last rent day",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'inform_about_last_rent_day'.")

        scheduler.add_job(
            inform_about_overdue_rent,
            trigger=CronTrigger(
                minute=f"*/{settings.NOTIFICATION_MAILING_INTERVAL_MINUTES}"
            ),
            # The `id` assigned to each job MUST be unique
            id="inform about overdue rent",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'inform about overdue rent'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
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
