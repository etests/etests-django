from django.utils.text import slugify
from collections import namedtuple
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SessionEvaluation:
    def __init__(self, test, session):
        self.totalMarks = 0
        self.sectionwiseMarks = [0 for i in range(len(test.sections))]
        self.test = test
        self.questions = test.questions
        self.session = session
        self.maxMarks = [0 for i in range(len(test.sections)+1)]
        self.questionWiseMarks = [{"marks":0,"status":0} for i in range(len(test.questions))]
        self.topicWiseMarks = [{} for i in range(len(test.sections))]

    def isListEmpty(self, l):
        if isinstance(l, list):
            return all( map(self.isListEmpty, l) )
        return False

    def markCorrect(self, i, curMarks=[]):
        if self.questions[i]['type'] in [0,2]:
            self.sectionwiseMarks[self.questions[i]['section']] += self.questions[i]['correctMarks']
            self.totalMarks += self.questions[i]['correctMarks']
            self.questionWiseMarks[i]['marks'] = self.questions[i]['correctMarks']
            self.questionWiseMarks[i]['status'] = 2 
        elif self.questions[i]['type']==1:
            if len(self.session['response'][i]['answer']) < len(self.test.answers[i]['answer']):
                marks = self.questions[i]['partialMarks']*len(self.session['response'][i]['answer'])
                self.sectionwiseMarks[self.questions[i]['section']] += marks
                self.totalMarks += marks
                self.questionWiseMarks[i]['marks'] = marks
                self.questionWiseMarks[i]['status'] = 3
            else:
                self.sectionwiseMarks[self.questions[i]['section']] += self.questions[i]['correctMarks']
                self.totalMarks += self.questions[i]['correctMarks']
                self.questionWiseMarks[i]['marks'] = self.questions[i]['correctMarks']
                self.questionWiseMarks[i]['status'] = 2
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
            self.questionWiseMarks[i]['marks'] = marks
            self.questionWiseMarks[i]['status'] = status
            

    def markIncorrect(self, i):
        self.sectionwiseMarks[self.questions[i]['section']] -= self.questions[i]['incorrectMarks']
        self.totalMarks -= self.questions[i]['incorrectMarks']
        self.questionWiseMarks[i]['marks'] = self.questions[i]['incorrectMarks']*(-1)
        self.questionWiseMarks[i]['status'] = 1

    def evaluate(self):
        for i in range(len(self.questions)):
            self.maxMarks[-1]+=self.questions[i]['correctMarks']
            self.maxMarks[self.questions[i]['section']]+=self.questions[i]['correctMarks']
            if self.isListEmpty(self.session['response'][i]['answer']):
                continue
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
                # For Matrix match for each part status 0 means unanswered 1 means incorrect 2 means correct
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

            currentTopic = self.topicWiseMarks[self.questions[i]['section']]
            if isinstance(self.questionWiseMarks[i]['marks'], list):
                marks = sum(self.questionWiseMarks[i]['marks'])
            else:
                marks = self.questionWiseMarks[i]['marks']
            if self.questions[i]['topicIndex'] in currentTopic:
                currentTopic[self.questions[i]['topicIndex']] += marks
            else:
                currentTopic[self.questions[i]['topicIndex']] = marks

        return [{
            "total": self.totalMarks,
            "sectionWise": self.sectionwiseMarks,
            "maxMarks": self.maxMarks
        },self.questionWiseMarks,self.topicWiseMarks]
    

def generateRanks(sessions):
        if not sessions or len(sessions)==0:
            return False

        for session in sessions:
            session.ranks = {}
            session.ranks['overall'] = 0
            session.ranks['sectionWise'] = []
            for section in range(len(session.marks['sectionWise'])):
                session.ranks['sectionWise'].append(0)

        marks_list = [[session.marks['total'], i] for (i,session) in enumerate(sessions)]
        sectionwise_marks_list = [[[session.marks['sectionWise'][j], i] for (i,session) in enumerate(sessions)] for j in range(len(sessions[0].marks['sectionWise']))]
        marks_list.sort()
        marks_list.reverse()


        total = 0
        sectionWiseTotal = [0 for i in range(len(sessions[0].marks['sectionWise']))]
        last_marks = 1000000
        last_rank = 1
        for (i, marks) in enumerate(marks_list):
            total += marks[0]
            if last_marks == marks[0]:
                sessions[marks[-1]].ranks['overall'] = last_rank
            else:
                sessions[marks[-1]].ranks['overall'] = i+1
                last_marks = marks[0]
                last_rank = i+1
            for j in range(len(sessions[marks[-1]].marks['sectionWise'])):
                sectionWiseTotal[j] += sessions[marks[-1]].marks['sectionWise'][j]

        for (i, sectionwise_marks) in enumerate(sectionwise_marks_list):
            sectionwise_marks.sort()
            sectionwise_marks.reverse()
            last_marks = 1000000
            last_rank = 1
            for (j, section_marks) in enumerate(sectionwise_marks):
                if last_marks == section_marks[0]:
                    sessions[section_marks[-1]].ranks['sectionWise'][i] = last_rank
                else:
                    sessions[section_marks[-1]].ranks['sectionWise'][i] = j+1
                    last_marks = section_marks[0]
                    last_rank = j+1

        return {
            "sessions": sessions,
            "stats":{
                "average": {
                    "overall": total/len(sessions),
                    "sectionWise": [sectionTotal/len(sessions) for sectionTotal in sectionWiseTotal]
                },
                "highest": {
                    "overall": marks_list[0][0],
                    "sectionWise": [section_marks[0][0] for section_marks in sectionwise_marks_list]
                }
            },
            "marks_list": {
                "overall": marks_list,
                "sectionWise": sectionwise_marks_list
            }
        }

def getRank(l, marks):
    lo=0
    hi=len(l)-1
    rank=len(l)+1
    while lo<len(l) and hi>=0 and lo<=hi:
        m = int((lo+hi)/2)
        if l[m][0] == marks:
            while m>=0 and l[m][0] == marks:
                rank = m+1
                m-=1
            break
        elif l[m][0] < marks:
            rank = m+1
            hi = m-1
        else:
            lo = m+1
    
    return rank

def getVirtualRanks(marks_list, marks_obtained):
    return {
        "overall": getRank(marks_list["overall"], marks_obtained["total"]),
        "sectionWise": [getRank(section_marks_list, marks_obtained["sectionWise"][i]) for (i,section_marks_list) in enumerate(marks_list["sectionWise"])]
    }


def send_mail(to,subject,body):
    email_id = to
    message = Mail(
        from_email=os.environ.get('EMAIL_ID'),
        to_emails = email_id,
        subject=subject,
        html_content=body)
    try:
        sg = SendGridAPIClient(os.environ.get('EMAIL_API_KEY'))
        response = sg.send(message)
        if response.status_code == 202:
            return True
        else:
            return False
    except Exception as e:
        print(e) 
        return False


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