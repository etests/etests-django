from api.models import Test


def evaluate_sessions():
    for test in Test.objects.filter(finished=False, marks_list__isnull=True):
        test.evaluate_sessions()


def auto_rank_declare():
    for test in Test.objects.filter(finished=False, marks_list__isnull=True):
        test.generate_ranks()
