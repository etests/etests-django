from django.utils.text import slugify
from collections import namedtuple

class SessionEvaluation:
    def __init__(self, test, session):
        self.total_marks = 0
        self.sectionwise_marks = [0 for i in range(len(test.sections))]
        self.test = test
        self.questions = test.questions
        self.session = session

    def markCorrect(self, question):
        self.sectionwise_marks[question['section']] += question['correctMarks']
        self.total_marks += question['correctMarks']

    def markIncorrect(self, question):
        self.sectionwise_marks[question['section']] += question['incorrectMarks']
        self.total_marks -= question['incorrectMarks']

    def evaluate(self):
        for i in range(len(self.questions)):
            if self.questions[i]['type']==0:
                if self.session['response'][i]['answer'] == self.test.answers[i]['answer']:
                    self.markCorrect(self.questions[i])
                else:
                    self.markIncorrect(self.questions[i])
                    
            elif self.questions[i]['type']==1:
                if(all(x in  self.test.answers[i]['answer'] for x in self.session['response'][i]['answer'])): 
                    self.markCorrect(self.questions[i])
                else:
                    self.markIncorrect(self.questions[i])
        return {
            "total": self.total_marks,
            "sectionwise": self.sectionwise_marks
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
    ModelClass = model_instance.__class__

    while ModelClass._default_manager.filter(
        **{slug_field_name: unique_slug}
    ).exists():
        unique_slug = '{}-{}'.format(slug, extension)
        extension += 1

    return unique_slug


def position_to_label(position):
    labels = ["A", "B", "C", "D"]
    if position>0 and position<=len(labels):
        return labels[position-1]
    return ''