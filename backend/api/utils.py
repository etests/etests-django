from django.utils.text import slugify
from collections import namedtuple

class SessionEvaluation:
    def __init__(self, test, session):
        self.totalMarks = 0
        self.sectionwiseMarks = [0 for i in range(len(test.sections))]
        self.test = test
        self.questions = test.questions
        self.session = session
        self.maxMarks = [0 for i in range(len(test.sections)+1)]
        self.questionwiseMarks = [{"marks":0,"status":0} for i in range(len(test.questions))]

    def markCorrect(self, i, curMarks=[]):
        if self.questions[i]['type'] in [0,2]:
            self.sectionwiseMarks[self.questions[i]['section']] += self.questions[i]['correctMarks']
            self.totalMarks += self.questions[i]['correctMarks']
            self.questionwiseMarks[i]['marks'] = self.questions[i]['correctMarks']
            self.questionwiseMarks[i]['status'] = 2 
        elif self.questions[i]['type']==1:
            if len(self.session['response'][i]['answer']) < len(self.test.answers[i]['answer']):
                marks = self.questions[i]['partialMarks']*len(self.session['response'][i]['answer'])
                self.sectionwiseMarks[self.questions[i]['section']] += marks
                self.totalMarks += marks
                self.questionwiseMarks[i]['marks'] = marks
                self.questionwiseMarks[i]['status'] = 3
            else:
                self.sectionwiseMarks[self.questions[i]['section']] += self.questions[i]['correctMarks']
                self.totalMarks += self.questions[i]['correctMarks']
                self.questionwiseMarks[i]['marks'] = self.questions[i]['correctMarks']
                self.questionwiseMarks[i]['status'] = 2
        elif self.questions[i]['type']==3:
            totalMatrixMarks = 0
            marks=[]
            status=[]
            for j in range(len(curMarks)):
                totalMatrixMarks +=curMarks[j]['marks']
                marks.append(curMarks[j]['marks'])
                status.append(curMarks[j]['status'])
            self.sectionwiseMarks[self.questions[i]['section']] += totalMatrixMarks
            self.totalMarks += totalMatrixMarks
            self.questionwiseMarks[i]['marks'] = marks
            self.questionwiseMarks[i]['status'] = status
            

    def markIncorrect(self, i):
        self.sectionwiseMarks[self.questions[i]['section']] -= self.questions[i]['incorrectMarks']
        self.totalMarks -= self.questions[i]['incorrectMarks']
        self.questionwiseMarks[i]['marks'] = self.questions[i]['incorrectMarks']*(-1)
        self.questionwiseMarks[i]['status'] = 1

    def evaluate(self):
        for i in range(len(self.questions)):
            self.maxMarks[-1]+=self.questions[i]['correctMarks']
            self.maxMarks[self.questions[i]['section']]+=self.questions[i]['correctMarks']
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
                curMarks = [{"marks":0,"status":0} for i in range(len(responses))]
                for j in range( len(responses) ):
                    if( len(responses[j])!=0 and sorted(responses[j]) == sorted(answers[j]) ):
                        curMarks[j]['marks']=self.questions[i]['partialMarks']
                        curMarks[j]['status']=2
                    else:
                        curMarks[j]['marks']=(self.questions[i]['incorrectMarks'])*(-1)
                        curMarks[j]['status']=1
                self.markCorrect(i,curMarks)

        return [{
            "total": self.totalMarks,
            "sectionWise": self.sectionwiseMarks,
            "maxMarks": self.maxMarks
        },self.questionwiseMarks]


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