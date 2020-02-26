from apscheduler.schedulers.background import BackgroundScheduler

from .email_tasks import student_reminder, email_institutes_test_report


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(student_reminder, "cron", day_of_week="wed,sat", hour="6")
    scheduler.add_job(
        email_institutes_test_report, "cron", day_of_week="thu,mon", hour="2"
    )
    scheduler.start()
