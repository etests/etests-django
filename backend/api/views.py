import json
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import APIException, MethodNotAllowed, PermissionDenied, NotFound, ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions
from .utils import SessionEvaluation, generateRanks
from .serializers import *
from .models import *
from .forms import *
from authentication.models import Institute
from django.contrib.auth.decorators import login_required

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

class FollowingInstitutesView(generics.ListAPIView):
    permission_classes = (IsStudentOwner,)
    serializer_class = FollowingInstitutesSerializer
    def get_queryset(self):
        if self.request.user.is_student:
            return Institute.objects.filter(following_students=self.request.user.student,verified=True)
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
            enrollment = Enrollment.objects.get(batch=batch, roll_number=roll_number)
            if enrollment.joining_key == joining_key:
                enrollment.student = request.user.student
            enrollment.save()
            return Response("Joined Successfully")
        except:
            raise ParseError("Invalid roll number or joining key!") 

class FollowInstituteView(APIView):
    permission_classes = (IsStudentOwner,)

    def post(self, request, id):
        try:
            institute = Institute.objects.get(id=id)
            if institute in request.user.student.following.all():
                return Response("Already following ;)")
            else:
                request.user.student.following.add(institute)
                return Response("Followed Successfully!")
        except Exception as e:
            print(e)
            raise ParseError("Sorry, you can't follow this institute!") 

class InstitutesListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Institute.objects.filter(verified=True)
        serializer = InstituteListSerializer(queryset, many=True)
        return Response(serializer.data)

class ExamListView(viewsets.ViewSet):
    permission_classes = (ReadOnly,)
    def list(self, request):
        queryset = Exam.objects.filter()
        serializer = ExamListSerializer(queryset, many=True)
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
                return Test.objects.filter(practice=False, institute=self.request.user.institute)
            elif self.request.user.is_student:
                return Test.objects.filter(practice=False, registered_students=self.request.user.student,visible=True)
            elif self.request.user.is_staff:
                return Test.objects.all()
        else:
            return None

class TestCreateView(generics.CreateAPIView):
    permission_classes = (IsInstituteOwner,)
    serializer_class = TestCreateSerializer

    def perform_create(self, serializer):
        test_series_ids = self.request.data.pop('test_series', None)
        exam_id = self.request.data.get('exam', None)
        if exam_id:
            try:
                exam = Exam.objects.get(id=exam_id)
                for test_series_id in test_series_ids:
                    try:
                        TestSeries.objects.get(id=test_series_id).exams.add(exam)
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
        serializer.save(institute=self.request.user.institute, registered_students=student_ids)
        
        
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
                "status": 0,
                "timeElapsed": 0
            })
        current = {
            "questionIndex": 0,
            "sectionIndex": 0
        }    
        session = Session.objects.create(student=self.request.user.student, test=test, response=response, result=[], current=current, practice=(test.practice or test.status>1))
        return session

    def retrieve(self, *args, **kwargs):
        test_id = kwargs['test_id']
        try:
            test=Test.objects.get(id=test_id)
        except:
            raise NotFound("This test does not exist.")
        try:
            session = Session.objects.get(test=test, student=self.request.user.student, completed=False)
        except:
            session = None
        if session:
            return Response(self.get_serializer(session).data)
        elif self.request.user.is_student:
            if self.request.user.student in test.registered_students.all():
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
            return Response(self.get_serializer(session).data)
        else:
            raise NotFound("Invalid Request.")
        

    def partial_update(self,*args,**kwargs):
        instance = self.get_object()
        session = self.request.data
        if session['completed']:
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

class ResultView(generics.RetrieveAPIView):
    permission_classes = (ReadOnly, permissions.IsAuthenticated)
    def get_serializer_class(self):
        session = self.get_object()
        test = session.test
        if test.status == 4:
            return ReviewSerializer
        else:
            return ResultSerializer
    def get_queryset(self):
        if self.request.user.is_student:
            return Session.objects.filter(student = self.request.user.student)
        elif self.request.user.is_institute:
            return Session.objects.filter(student__institutes = self.request.user.institute)
        elif self.request.user.is_staff:
            return Session.objects.all()
        return None

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
    permission_classes = (IsInstituteOwner,)
    def post(self, request, id):
        try:
            test = Test.objects.get(id=id)
        except Exception as e:
            print(e)
            raise NotFound("No such Test!")
        if test.practice:
            raise PermissionDenied("Ranks cannot be generated for practice tests.")  
        if test.status <=1:
            raise PermissionDenied("Ranks can be generated only after test closes.")  
        elif test.status in [2,3]:
            sessions = Session.objects.filter(test = test, practice = False)
            generated = generateRanks(sessions)
            Session.objects.bulk_update(generated.pop("sessions", None), ["ranks"])
            test.stats = generated
            test.finished = True
            test.save()
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