import os
import random
import string
from collections import namedtuple
from importlib import import_module

from django.utils.text import slugify
from six import string_types


def random_key(length=8):
    return "".join(
        random.choice(string.ascii_letters + string.digits) for i in range(length)
    )


def unique_random_key(instance):
    new_key = random_key()

    Klass = instance.__class__

    qs_exists = Klass.objects.filter(joining_key=new_key).exists()
    if qs_exists:
        return random_key(instance)
    return new_key


def import_callable(path_or_callable):
    if hasattr(path_or_callable, "__call__"):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit(".", 1)
        return getattr(import_module(package), attr)


class SessionEvaluation:
    def __init__(self, session):
        self.test = session.test
        self.session = session
        self.total_marks = 0
        self.section_wise_marks = [0] * len(self.test.sections)
        self.questions = self.test.questions
        self.max_marks = [0] * (len(self.test.sections) + 1)
        self.question_wise_marks = [{"marks": 0, "status": 0}] * len(self.questions)
        self.topic_wise_marks = [{}] * len(self.test.sections)

    def is_list_empty(self, l):
        if isinstance(l, list):
            return all(map(self.is_list_empty, l))
        return False

    def mark_correct(self, i, cur_marks=[]):
        if self.questions[i]["type"] in [0, 2]:
            self.section_wise_marks[self.questions[i]["section"]] += self.questions[i][
                "correct_marks"
            ]
            self.total_marks += self.questions[i]["correct_marks"]
            self.question_wise_marks[i]["marks"] = self.questions[i]["correct_marks"]
            self.question_wise_marks[i]["status"] = 2
        elif self.questions[i]["type"] == 1:
            if len(self.session.response[i]["answer"]) < len(
                self.test.answers[i]["answer"]
            ):
                marks = self.questions[i]["partial_marks"] * len(
                    self.session.response[i]["answer"]
                )
                self.section_wise_marks[self.questions[i]["section"]] += marks
                self.total_marks += marks
                self.question_wise_marks[i]["marks"] = marks
                self.question_wise_marks[i]["status"] = 3
            else:
                self.section_wise_marks[self.questions[i]["section"]] += self.questions[
                    i
                ]["correct_marks"]
                self.total_marks += self.questions[i]["correct_marks"]
                self.question_wise_marks[i]["marks"] = self.questions[i][
                    "correct_marks"
                ]
                self.question_wise_marks[i]["status"] = 2
        elif self.questions[i]["type"] == 3:
            total_matrix_marks = 0
            marks = []
            status = []
            for j in range(len(cur_marks)):
                total_matrix_marks += cur_marks[j]["marks"]
                marks.append(cur_marks[j]["marks"])
                status.append(cur_marks[j]["status"])
            self.section_wise_marks[self.questions[i]["section"]] += total_matrix_marks
            self.total_marks += total_matrix_marks
            self.question_wise_marks[i]["marks"] = marks
            self.question_wise_marks[i]["status"] = status

    def mark_incorrect(self, i):
        self.section_wise_marks[self.questions[i]["section"]] -= self.questions[i][
            "incorrect_marks"
        ]
        self.total_marks -= self.questions[i]["incorrect_marks"]
        self.question_wise_marks[i]["marks"] = self.questions[i]["incorrect_marks"] * (
            -1
        )
        self.question_wise_marks[i]["status"] = 1

    def evaluate(self):
        for i in range(len(self.questions)):
            if self.questions[i]["type"] == 3:
                self.max_marks[-1] += self.questions[i]["partial_marks"] * len(
                    self.test.answers[i]["answer"]
                )
                self.max_marks[self.questions[i]["section"]] += self.questions[i][
                    "partial_marks"
                ] * len(self.test.answers[i]["answer"])
            else:
                self.max_marks[-1] += self.questions[i]["correct_marks"]
                self.max_marks[self.questions[i]["section"]] += self.questions[i][
                    "correct_marks"
                ]

            if self.is_list_empty(self.session.response[i]["answer"]):
                continue
            if self.questions[i]["type"] == 0:
                if self.session.response[i]["answer"] == self.test.answers[i]["answer"]:
                    self.mark_correct(i)
                else:
                    self.mark_incorrect(i)

            elif self.questions[i]["type"] == 1:
                if self.questions[i]["partial_marks"] > 0 and all(
                    x in self.test.answers[i]["answer"]
                    for x in self.session.response[i]["answer"]
                ):
                    self.mark_correct(i)
                elif (
                    sorted(self.session.response[i]["answer"])
                    == self.test.answers[i]["answer"]
                ):
                    self.mark_correct(i)
                else:
                    self.mark_incorrect(i)
            elif self.questions[i]["type"] == 2:
                given_response = float(self.session.response[i]["answer"])
                correct_answer = float(self.test.answers[i]["answer"])
                if (
                    0.99 * correct_answer <= given_response
                    and given_response <= 1.01 * correct_answer
                ):
                    self.mark_correct(i)
                else:
                    self.mark_incorrect(i)
            elif self.questions[i]["type"] == 3:
                # For Matrix match for each part status 0 means unanswered 1 means incorrect 2 means correct
                responses = self.session.response[i]["answer"]
                answers = self.test.answers[i]["answer"]
                cur_marks = [{"marks": 0, "status": 0} for i in range(len(responses))]
                for j, response in enumerate(responses):
                    if not response:
                        continue
                    elif response and sorted(response) == sorted(answers[j]):
                        cur_marks[j]["marks"] = self.questions[i]["partial_marks"]
                        cur_marks[j]["status"] = 2
                    else:
                        cur_marks[j]["marks"] = (
                            self.questions[i]["incorrect_marks"]
                        ) * (-1)
                        cur_marks[j]["status"] = 1
                self.mark_correct(i, cur_marks)

            current_topic = self.topic_wise_marks[self.questions[i]["section"]]
            if isinstance(self.question_wise_marks[i]["marks"], list):
                marks = sum(self.question_wise_marks[i]["marks"])
            else:
                marks = self.question_wise_marks[i]["marks"]
            if self.questions[i]["topic_index"] in current_topic:
                current_topic[self.questions[i]["topic_index"]] += marks
            else:
                current_topic[self.questions[i]["topic_index"]] = marks

        self.total_marks = round(self.total_marks, 2)
        self.section_wise_marks = [round(marks, 2) for marks in self.section_wise_marks]
        self.topic_wise_marks = [
            {
                topic: round(self.topic_wise_marks[i][topic], 2)
                for topic in self.topic_wise_marks[i].keys()
            }
            for i in range(len(self.test.sections))
        ]

        self.session.marks = {
            "total": self.total_marks,
            "section_wise": self.section_wise_marks,
            "max_marks": self.max_marks,
        }
        self.session.result = {
            "question_wise_marks": self.question_wise_marks,
            "topic_wise_marks": self.topic_wise_marks,
        }
        self.session.completed = True

def generate_ranks(sessions):
    if not sessions:
        return False

    for session in sessions:
        session.ranks = {}
        session.ranks["overall"] = 0
        session.ranks["section_wise"] = [0] * len(session.marks["section_wise"])

    marks_list = [[session.marks["total"], i] for (i, session) in enumerate(sessions)]
    section_wise_marks_list = [
        [[session.marks["section_wise"][j], i] for (i, session) in enumerate(sessions)]
        for j in range(len(sessions[0].marks["section_wise"]))
    ]
    marks_list.sort()
    marks_list.reverse()

    total = 0
    section_wise_total = [0 for i in range(len(sessions[0].marks["section_wise"]))]
    last_marks = 1000000
    last_rank = 1
    for (i, marks) in enumerate(marks_list):
        total += marks[0]
        if last_marks == marks[0]:
            sessions[marks[-1]].ranks["overall"] = last_rank
        else:
            sessions[marks[-1]].ranks["overall"] = i + 1
            last_marks = marks[0]
            last_rank = i + 1
        for j in range(len(sessions[marks[-1]].marks["section_wise"])):
            section_wise_total[j] += sessions[marks[-1]].marks["section_wise"][j]

    for (i, section_wise_marks) in enumerate(section_wise_marks_list):
        section_wise_marks.sort()
        section_wise_marks.reverse()
        last_marks = 1000000
        last_rank = 1
        for (j, section_marks) in enumerate(section_wise_marks):
            if last_marks == section_marks[0]:
                sessions[section_marks[-1]].ranks["section_wise"][i] = last_rank
            else:
                sessions[section_marks[-1]].ranks["section_wise"][i] = j + 1
                last_marks = section_marks[0]
                last_rank = j + 1

    return {
        "sessions": sessions,
        "stats": {
            "average": {
                "overall": total / len(sessions),
                "section_wise": [
                    sectionTotal / len(sessions) for sectionTotal in section_wise_total
                ],
            },
            "highest": {
                "overall": marks_list[0][0],
                "section_wise": [
                    section_marks[0][0] for section_marks in section_wise_marks_list
                ],
            },
        },
        "marks_list": {"overall": marks_list, "section_wise": section_wise_marks_list},
    }


def get_rank(l, marks):
    lo = 0
    hi = len(l) - 1
    rank = len(l) + 1
    while lo < len(l) and hi >= 0 and lo <= hi:
        m = int((lo + hi) / 2)
        if l[m][0] == marks:
            while m >= 0 and l[m][0] == marks:
                rank = m + 1
                m -= 1
            break
        elif l[m][0] < marks:
            rank = m + 1
            hi = m - 1
        else:
            lo = m + 1

    return rank


def virtual_rank(marks_list, marks_obtained):
    return {
        "overall": get_rank(marks_list["overall"], marks_obtained["total"]),
        "section_wise": [
            get_rank(section_marks_list, marks_obtained["section_wise"][i])
            for (i, section_marks_list) in enumerate(marks_list["section_wise"])
        ],
    }


def get_unique_slug(model_instance, slugable_field_name, slug_field_name="slug"):
    """
    Takes a model instance, sluggable field name (such as 'title') of that
    model as string, slug field name (such as 'slug') of the model as string;
    returns a unique slug as string.
    """
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    model_class = model_instance.__class__

    while model_class._default_manager.filter(
        **{slug_field_name: unique_slug}
    ).exists():
        unique_slug = "{}-{}".format(slug, extension)
        extension += 1

    return unique_slug


def position_to_label(position):
    labels = ["A", "B", "C", "D"]
    if position > 0 and position <= len(labels):
        return labels[position - 1]
    return ""
