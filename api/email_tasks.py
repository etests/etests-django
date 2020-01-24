from .ses import send_email
from .models import Institute, Test
from django.db.models import Count
from datetime import date, timedelta
from django.template.loader import render_to_string

def email_institutes_test_report(days=5):
    for institute in Institute.objects.filter(verified=True):
        last_n_days_tests = Test.objects.filter(
            institute=institute, date_added__gte=date.today() - timedelta(days=days)
        )
        tests_count = last_n_days_tests.count()
        tests_sessions_counts = last_n_days_tests.annotate(
            session_count=Count("sessions")
        )
        send_email(
            institute.user.email,
            render_to_string("institute_test_report/subject.txt"),
            render_to_string(
                "institute_test_report/body.html",
                {
                    "name": institute.user.name,
                    "n": days,
                    "tests_count": tests_count,
                    "tests_sessions_counts": tests_sessions_counts,
                },
            ),
        )
