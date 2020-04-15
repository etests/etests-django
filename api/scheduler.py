from apscheduler.schedulers.background import BackgroundScheduler

# from api.tasks.email_tasks import student_reminder, email_institutes_test_report
from api.tasks.test_tasks import evaluate_sessions, auto_rank_declare


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(student_reminder, "cron", day_of_week="wed,sat", hour="6")
    # scheduler.add_job(
    # email_institutes_test_report, "cron", day_of_week="thu,mon", hour="2"
    # )
    scheduler.add_job(evaluate_sessions, "cron", day_of_week="*", hour="2")
    scheduler.add_job(auto_rank_declare, "cron", day_of_week="*", hour="2")
    scheduler.start()
