from api.ses import send_email
from api.models import Institute, Test, Student, Session
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string


def student_reminder(days=4):
    for student in Student.objects.all():
        last_n_days_sessions = student.sessions.filter(
            checkin_time__gte=timezone.now() - timedelta(days=days)
        )
        sessions_count = last_n_days_sessions.count()
        send_email(
            student.user.email,
            render_to_string("student_reminder/subject.txt"),
            render_to_string(
                "student_reminder/body.html",
                {
                    "name": student.user.name,
                    "n": days,
                    "sessions_count": sessions_count,
                },
            ),
        )


def email_institutes_test_report(days=5):
    for institute in Institute.objects.filter(verified=True):
        last_n_days_tests = institute.tests.filter(
            date_added__gte=timezone.now() - timedelta(days=days)
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
