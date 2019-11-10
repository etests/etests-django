import json
import os
from datetime import date
from random import choice, randint
from string import digits

from django.apps import apps
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import (APIException, MethodNotAllowed,
                                       NotFound, ParseError, PermissionDenied)
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Institute

from .forms import *
from .models import *
from .serializers import *
from .utils import SessionEvaluation, generateRanks, getVirtualRanks, send_mail


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

class IsInstituteOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_institute

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_institute and (not obj.institute or obj.institute == request.user.institute)

class IsStudentOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_student and (not obj.student or obj.student == request.user.student)

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and  obj.user == request.user

class BatchListView(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = BatchListSerializer
    def get_queryset(self):
        if self.request.user.is_student:
            return Batch.objects.filter(institute__in=self.request.user.student.institutes)
        elif self.request.user.is_institute:
            return Batch.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_staff:
            return Batch.objects.all()
        else:
            return None

class JoinedInstitutesView(generics.ListAPIView):
    permission_classes = (IsStudentOwner,)
    serializer_class = JoinedInstitutesSerializer
    def get_queryset(self):
        if self.request.user.is_student:
            return Institute.objects.filter(students=self.request.user.student, verified=True)
        else:
            return None

class BatchListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = InstituteBatchSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Batch.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Batch.objects.all()
        else:
            return None
    
    def perform_create(self, serializer):
        serializer.save(institute=self.request.user.institute)
    

class BatchRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = InstituteBatchSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Batch.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Batch.objects.all()
        else:
            return None


class BatchJoinView(APIView):
    permission_classes = (IsStudentOwner,)

    def post(self, request):
        roll_number = request.data['rollNumber']
        joining_key = request.data['joiningKey']
        try:
            batch = Batch.objects.get(id=self.request.data['batch'])
            enrollment = Enrollment.objects.get(batch = batch, roll_number=roll_number)
            if enrollment.joining_key == joining_key:
                enrollment.student = request.user.student
                enrollment.date_joined = datetime.now()
                enrollment.save()
                # Feature required: Register this student to all the previous tests of this batch
                return Response("Joined Successfully")
            else:
                raise ParseError("Invalid roll number or joining key!")
        except:
            raise ParseError("Invalid roll number or joining key!") 

class InstitutesListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Institute.objects.filter(verified=True, show=True)
        serializer = InstituteListSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

class ExamListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Exam.objects.filter()
        serializer = ExamListSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)
        
class SubjectListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Subject.objects.filter()
        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data)
        
class TopicListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Topic.objects.filter()
        serializer = TopicSerializer(queryset, many=True)
        return Response(serializer.data)
        
class TagListView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

class TestSeriesListView(generics.ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = TestSeriesSerializer
    def get_queryset(self):
        return TestSeries.objects.filter(institute__verified=True, visible=True)
        
class TestSeriesListCreateView(generics.ListCreateAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = TestSeriesSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return TestSeries.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_student:
            return TestSeries.objects.filter(registered_students = self.request.user.student,visible=True,institute__verified=True)
        elif self.request.user.is_staff:
            return TestSeries.objects.all()
        return None
    
    def perform_create(self, serializer):
        serializer.save(institute=self.request.user.institute)
    

class TestSeriesRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = TestSeriesSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return TestSeries.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return TestSeries.objects.all()
        else:
            return None


class TestListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get_serializer_class(self):
        if self.request.user.is_student:
            return StudentTestListSerializer
        else:
            return TestListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(aits = False, institute = self.request.user.institute)
            elif self.request.user.is_student:
                return Test.objects.filter(aits = False, registered_students = self.request.user.student, visible = True)
            elif self.request.user.is_staff:
                return Test.objects.all()
        else:
            return None

class FreeTestListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get_serializer_class(self):
        return StudentTestListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_student:
                return Test.objects.filter(free=True, sessions__student = self.request.user.student, visible = True).distinct()
        else:
            return None

class TestCreateView(generics.CreateAPIView):
    permission_classes = (IsInstituteOwner,)
    serializer_class = TestCreateSerializer

    def perform_create(self, serializer):
        test_series_ids = self.request.data.pop('test_series', None)
        exam_id = self.request.data.get('exam', None)
        free = self.request.data.get('free', False)
        print(self.request.data)
        if exam_id:
            try:
                exam = Exam.objects.get(id=exam_id)
                for test_series_id in test_series_ids:
                    try:
                        test_series = TestSeries.objects.get(id=test_series_id)
                        test_series.exams.add(exam)
                        if test_series.price == 0:
                            free = True
                    except:
                        pass
            except Exception as e:
                pass
        batches = self.request.data.pop('batches', None)
        student_ids = []
        if batches:
            for batch_id in batches:
                try:
                    batch = Batch.objects.get(id = batch_id)
                    if batch.institute == self.request.user.institute:
                        student_ids += [student.id for student in batch.students()]
                except Exception as e:
                    pass
        serializer.save(institute=self.request.user.institute, registered_students=student_ids, free = free)
        
        
class TestRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = TestSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_institute:
                return Test.objects.filter(institute=self.request.user.institute)
            elif self.request.user.is_staff:
                return Test.objects.all()
        else:
            return None

class SessionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsStudentOwner | permissions.IsAdminUser,)
    
    serializer_class = SessionSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Session.objects.all()
        elif self.request.user.is_student:
            return Session.objects.filter(student=self.request.user.student)
        return None

    def create_session(self, test):
        response = []
        for i in range(len(test.questions)):
            response.append({
                "answer": [],
                "status": 1,
                "timeElapsed": 0
            })
        current = {
            "questionIndex": 0,
            "sectionIndex": 0
        }    
        session = Session.objects.create(student=self.request.user.student, test=test, response=response, result=[], current=current, practice=(test.status>1), duration=test.time_alotted)
        return session

    def retrieve(self, *args, **kwargs):
        test_id = kwargs['test_id']
        try:
            test=Test.objects.get(id=test_id)
        except:
            raise NotFound("This test does not exist.")
        try:
            session = Session.objects.get(test=test, student=self.request.user.student, completed=False)
            if test.status >= 2 and not session.practice:
                session.completed = True
                session.save()
                session = None
        except:
            session = None
        if session:
            if session.practice:
                self.serializer_class = PracticeSessionSerializer
            return Response(self.get_serializer(session).data)
        elif self.request.user.is_student:
            if self.request.user.student in test.registered_students.all() or test.free:
                sessions = Session.objects.filter(test=test, student=self.request.user.student)
                if test.status == 0:
                    raise ParseError("This test is not active yet.")
                elif test.status == 1 and len(sessions) == 0 or test.status>1:
                    session = self.create_session(test)
                elif test.status == 1 and len(sessions):
                    raise ParseError("You have already attempted this test. You can attempt this test in practice mode after result declaration.")
            else:
                raise ParseError("You are not registered for this test.")
        else:
            raise PermissionDenied("You cannot attempt this test.")
        if session:
            if session.practice:
                self.serializer_class = PracticeSessionSerializer
            return Response(self.get_serializer(session).data)
        else:
            raise NotFound("Invalid Request.")
        

    def partial_update(self,*args,**kwargs):
        instance = self.get_object()
        session = self.request.data
        if session['practice']:
            if instance.completed:
                raise PermissionDenied("You have already submitted this test.")
            else:
                self.serializer_class = PracticeSessionSerializer
                if instance.test.marks_list is not None:
                    instance.ranks = getVirtualRanks(instance.test.marks_list, session["marks"])
        elif session['completed']:
            self.serializer_class = ResultSerializer
            if instance.completed:
                raise PermissionDenied("You have already submitted this test.")
            else: 
                test = Test.objects.get(id=instance.test.id)
                evaluated = SessionEvaluation(test, session).evaluate()
                instance.marks = evaluated[0]
                instance.result = {"questionWiseMarks": evaluated[1], "topicWiseMarks": evaluated[2]}
        serializer = self.get_serializer(instance, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class EvaluateLeftSessions(APIView):
    permission_classes = (permissions.IsAdminUser,)
    
    def post(self, request, test_id):
        try:
            test = Test.objects.get(id = test_id)
            sessions = Session.objects.filter(test = test, marks__isnull=True)
            for session in sessions:
                evaluated = SessionEvaluation(session.test, SessionSerializer(session).data).evaluate()
                session.marks = evaluated[0]
                session.result = {"questionWiseMarks": evaluated[1], "topicWiseMarks": evaluated[2]}
                session.completed = True
            Session.objects.bulk_update(sessions, ["marks", "result", "completed"])
            return Response("Done!", status=status.HTTP_201_CREATED)
        except:
            raise ParseError("Some error ocurred")

def updateTestRanks(test):
    sessions = Session.objects.filter(test = test)
    if len(sessions) == 0:
        test.finished = True
        test.save()
        return False
    generated = generateRanks(sessions)
    if generated:
        Session.objects.bulk_update(generated.get("sessions", None), ["ranks"])
        test.marks_list = generated.get("marks_list", None)
        test.stats = generated.get("stats", None)
        test.finished = True
        test.save()
        return True
    return False

class ResultView(generics.RetrieveAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    def get_serializer_class(self):
        session = self.get_object()
        test = session.test
        if session.practice or test.status == 4:
            return ReviewSerializer
        else:
            return ResultSerializer

    def get_queryset(self):
        if self.request.user.is_student:
            return Session.objects.filter(student = self.request.user.student)
        elif self.request.user.is_institute:
            return Session.objects.filter(test__institute = self.request.user.institute)
        elif self.request.user.is_staff:
            return Session.objects.all()
        return None

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()

        if instance.marks is None:
            instance.completed = True
            evaluated = SessionEvaluation(instance.test, SessionSerializer(instance).data).evaluate()
            instance.marks = evaluated[0]
            instance.result = {"questionWiseMarks": evaluated[1], "topicWiseMarks": evaluated[2]}
            instance.save()

        return Response(self.get_serializer(instance).data)

class Review(generics.RetrieveAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = ReviewSerializer
    def get_queryset(self):
        if self.request.user.is_institute:
            return Session.objects.filter(student__institutes = self.request.user.institute)
        if self.request.user.is_student:
            return Session.objects.filter(student = self.request.user.student)
        elif self.request.user.is_staff:
            return Session.objects.all()
        return None

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        if instance.result or (instance.result and len(instance.result)!=0):
            return Response(self.get_serializer(instance).data)
        else:
            raise ParseError("You cannot review this test yet.")

class GenerateRanks(APIView):
    permission_classes = (IsInstituteOwner|permissions.IsAdminUser,)
    def post(self, request, id):
        try:
            test = Test.objects.get(id=id)
        except Exception as e:
            print(e)
            raise NotFound("No such Test!")
        if (test.practice or test.aits) and not request.user.is_staff:
            raise PermissionDenied("Ranks cannot be generated for this test.")  
        if test.status <=1:
            raise PermissionDenied("Ranks can be generated only after test closes.")  
        elif test.status in [2,3] or request.user.is_staff:
            updateTestRanks(test)
            return Response("Ranks generated.", status=status.HTTP_201_CREATED)
        else:
            raise ParseError("Final ranks are already declared.")                  

class RankListView(APIView):
    permission_classes = (IsInstituteOwner,)

    def get(self, request, id):
        sessions = Session.objects.filter(test__id=id, practice=False)
        serializer = RankListSerializer(sessions, many = True)
        return Response(serializer.data)
    

class TransactionListView(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        if self.request.user.is_institute:
            return Transaction.objects.filter(institute=self.request.user.institute)
        return None

class AITSTransactionListView(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = AITSTransactionSerializer
    
    def get_queryset(self):
        if self.request.user.is_institute:
            return AITSTransaction.objects.filter(institute=self.request.user.institute)
        return None

class CreditListView(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = CreditUseSerializer
    def get_queryset(self):
        if self.request.user.is_institute:
            return CreditUse.objects.filter(institute=self.request.user.institute)
        return None



class EnrollmentView(generics.ListCreateAPIView):
    permission_classes = (IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Enrollment.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_staff:
            return Enrollment.objects.all()
        return None

    def create(self, request, *args, **kwargs):
        enrollments = []
        headers = []
        data=[{
                'institute': request.user.institute.id,
                'batch':  request.data['batch'],
                'roll_number': roll_number 
            }
            for roll_number in request.data['rollNumbers']
            ]
            
        serializer = self.get_serializer(data = data, many = True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

class PaymentView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            send_mail( payment.user.email, 'Payment Verification in Progress', 'Your payment of Rs.'+str(payment.test_series.price)+ ' for '+payment.test_series.name+' will be verified shortly. The AITS will appear on your dashboard after payment is verified. If you have any query feel free to email us at help@etests.co.in') 
            return Response("Successful", status=status.HTTP_201_CREATED)
        else:
            raise ParseError("Invalid") 

class EnrollmentRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ReadOnly | IsInstituteOwner | permissions.IsAdminUser,)
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_institute:
            return Enrollment.objects.filter(institute=self.request.user.institute)
        elif self.request.user.is_student:
            return Enrollment.objects.filter(institute=self.request.user.student.institute)
        elif self.request.user.is_staff:
            return Enrollment.objects.all()
        else:
            return None


class ResetCodeCreateView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        email_id = request.data.get('email', None)
        user = User.objects.filter(email=email_id)
        if len(user):
            user = user[0]
            instance = ResetCode.objects.filter(user=user,done=False,date_added=date.today())
            if len(instance) == 0:
                reset_code=(''.join(choice(digits) for i in range(6)))
                ResetCode.objects.create(user=user,reset_code=reset_code)
            else:
                reset_code = instance[0].reset_code
            if send_mail( email_id, 'Password Reset', 'The Password Reset Code for eTests is '+'<strong>'+reset_code+'</strong>'):
                return Response("Password reset code sent successfully!", status=status.HTTP_201_CREATED)
            else:
                raise ParseError("Some error occured.")
        else:
            raise ParseError("No user with this email id.")

class ResetCodeSuccessView(APIView):    
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        reset_code = request.data.get("reset_code", None)
        password = request.data.get("password", None)
        try:
            instance =  ResetCode.objects.get(reset_code = reset_code, done=False, date_added=date.today())
            if password:
                instance.user.set_password(password)
                instance.user.save()
                instance.done=True
                instance.save()
                return  Response("Password changed successfully!", status=status.HTTP_201_CREATED)
            else:
                raise ParseError("Password cannot be empty.")
        except:
            raise ParseError("Invalid reset code.")


class ChangePasswordView(APIView):    
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        old_password = request.data.get("old_password", None)
        new_password = request.data.get("new_password",None)
        if old_password and new_password:
            user = authenticate(email=request.user.email , password=old_password)
            if user is not None:
                # A backend authenticated the credentials
                user.set_password(new_password)
                user.save()
                return  Response("Password changed successfully!", status=status.HTTP_201_CREATED)
            else:
                # No backend authenticated the credentials
                raise ParseError("Incorrect Password")
        else:
            raise ParseError("Password Cannot be Empty")

class AITSBuyer(generics.ListAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    serializer_class = AITSBuyerSerializer
    def get_queryset(self):
        if self.request.user.is_institute:
            return Payment.objects.filter(test_series__institute=self.request.user.institute,verified=True,show=True)
        elif self.request.user.is_staff:
            return Payment.objects.filter(verified=True,show=True)
        else:
            return None



class PublishTestSeries(APIView):
    permission_classes = (permissions.IsAdminUser | IsInstituteOwner,)
    def post(self,request):
        try:
            instance = TestSeries.objects.get(id=request.data.get("id"))
            instance.visible = True
            instance.save()
            return  Response("AITS Published Sucessfully!", status=status.HTTP_201_CREATED)
        except:
            raise ParseError("Cannot publish this AITS.")


class UploadQuestionImageView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        request.FILES["file"] = request.FILES.pop("upload")[0]
        form = QuestionImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return JsonResponse({
                "uploaded": 1,
                "fileName": image.file.name,
                "url": image.file.url
            })
        else:
            return JsonResponse({
                "uploaded": 0,
                "error": {
                    "message": form.errors.as_text()
                }
            })

class AddQuestionAPIView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = QuestionSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveQuestionAPIView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = QuestionSerializer
    
    def post(self, request):
        params = request.data
        type = params.get("type", None)
        difficulty = params.get("difficulty", None)
        subjectIndex = params.get("subjectIndex", None)
        topicIndex = params.get("topicIndex", None)

        questions = Question.objects.all()
        if type:
            questions = questions.filter(type = type)
        if difficulty:
            questions = questions.filter(difficulty = difficulty)
        if subjectIndex:
            questions = questions.filter(subjectIndex = subjectIndex)
            if topicIndex:
                questions = questions.filter(topicIndex = topicIndex)

        try:
            count = questions.count()
            serializer = self.serializer_class(questions[randint(0, count - 1)])
            return Response(serializer.data)
        except:
            raise NotFound("No matching question!")
