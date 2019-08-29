from django.utils.text import slugify
from collections import namedtuple

class SessionEvaluation:
    def __init__(self, test, session):
        self.total_marks = 0
        self.sectionwise_marks = [0 for i in range(len(test.sections))]
        self.test = test
        self.questions = test.questions
        self.session = session
        self.max_marks = [0 for i in range(len(test.sections)+1)]
        self.questionwise_marks = [{"marks":0,"status":0} for i in range(len(test.questions))]

    def markCorrect(self, i, cur_marks=[]):
        if self.questions[i]['type'] in [0,2]:
            self.sectionwise_marks[self.questions[i]['section']] += self.questions[i]['correctMarks']
            self.total_marks += self.questions[i]['correctMarks']
            self.questionwise_marks[i]['marks'] = self.questions[i]['correctMarks']
            self.questionwise_marks[i]['status'] = 2 
        elif self.questions[i]['type']==1:
            if len(self.session['response'][i]['answer']) < len(self.test.answers[i]['answer']):
                marks = self.questions[i]['partialMarks']*len(self.session['response'][i]['answer'])
                self.sectionwise_marks[self.questions[i]['section']] += marks
                self.total_marks += marks
                self.questionwise_marks[i]['marks'] = marks
                self.questionwise_marks[i]['status'] = 3
            else:
                self.sectionwise_marks[self.questions[i]['section']] += self.questions[i]['correctMarks']
                self.total_marks += self.questions[i]['correctMarks']
                self.questionwise_marks[i]['marks'] = self.questions[i]['correctMarks']
                self.questionwise_marks[i]['status'] = 2
        elif self.questions[i]['type']==3:
            total_matrix_marks = 0
            marks=[]
            status=[]
            for j in range(len(cur_marks)):
                total_matrix_marks +=cur_marks[j]['marks']
                marks.append(cur_marks[j]['marks'])
                status.append(cur_marks[j]['status'])
            self.sectionwise_marks[self.questions[i]['section']] += total_matrix_marks
            self.total_marks += total_matrix_marks
            self.questionwise_marks[i]['marks'] = marks
            self.questionwise_marks[i]['status'] = status
            

    def markIncorrect(self, i):
        self.sectionwise_marks[self.questions[i]['section']] -= self.questions[i]['incorrectMarks']
        self.total_marks -= self.questions[i]['incorrectMarks']
        self.questionwise_marks[i]['marks'] = self.questions[i]['incorrectMarks']*(-1)
        self.questionwise_marks[i]['status'] = 1

    def evaluate(self):
        for i in range(len(self.questions)):
            self.max_marks[-1]+=self.questions[i]['correctMarks']
            self.max_marks[self.questions[i]['section']]+=self.questions[i]['correctMarks']
            if self.questions[i]['type'] ==0:
                if self.session['response'][i]['answer'] == self.test.answers[i]['answer']:
                    self.markCorrect(i)
                else:
                    self.markIncorrect(i)
                    
            elif self.questions[i]['type']==1:
                if( self.questions[i]['partialMarks']>0 and all(x in  self.test.answers[i]['answer'] for x in self.session['response'][i]['answer'])): 
                    self.markCorrect(i)
                elif(sorted(self.session['response'][i]['answer'])==self.test.answers[i]['answer']):
                     self.markCorrect(i)
                else:
                    self.markIncorrect(i)
            elif self.questions[i]['type']==2:
                if( 0.99<=float(self.session['response'][i]['answer'])/float(self.test.answers[i]['answer']) <=1.01 ):
                    self.markCorrect(i)
                else:
                    self.markIncorrect(i)
            elif self.questions[i]['type']==3: 
                #For Matrix match for each part status 0 means unanswered 1 means incorrect 2 means correct
                responses=self.session['response'][i]['answer']
                answers = self.test.answers[i]['answer']
                cur_marks = [{"marks":0,"status":0} for i in range(len(responses))]
                for j in range( len(responses) ):
                    if( len(responses[j])!=0 and sorted(responses[j]) == sorted(answers[j]) ):
                        cur_marks[j]['marks']=self.questions[i]['partialMarks']
                        cur_marks[j]['status']=2
                    else:
                        cur_marks[j]['marks']=(self.questions[i]['incorrectMarks'])*(-1)
                        cur_marks[j]['status']=1
                self.markCorrect(i,cur_marks)

        return [{
            "total": self.total_marks,
            "sectionwise": self.sectionwise_marks,
            "max_marks":self.max_marks
        },self.questionwise_marks]


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