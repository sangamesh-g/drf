from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import EmployeeSerializer
from employees.models import Employee
from django.http import Http404

class employees(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class employee_detail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employee = self.get_object(pk)
        if employee is None:
            return Response(status=404)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        if employee is None:
            return Response(status=404)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        if employee is None:
            return Response(status=404)
        employee.delete()
        return Response(status=204)
    

from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle

class RegisterView(APIView):
    permission_classes=[]
    throttle_classes=[ScopedRateThrottle]
    throttle_scope="register"


    def post(self,request):
        serializer=RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user=serializer.save()

        return Response({
            "message":"User registered successfully",
            'user':user.username
        },
        status=status.HTTP_201_CREATED
        )
    

from .serializers import LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    serializer_class=LoginSerializer


from celery.result import AsyncResult
from celery.app.control import Control
from .tasks import process_report
from ST.celery import app
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class StartReportAPIView(APIView):
    """
    Covers:
    - .delay()
    - immediate response
    """

    def post(self, request):
        report_id = request.data.get("report_id")

        task = process_report.delay(report_id)

        return Response({
            "task_id": task.id,
            "message": "Report processing started"
        }, status=202)


class ReportStatusAPIView(APIView):
    """
    Covers:
    - task status
    - redis progress
    """

    def get(self, request, task_id):
        result = AsyncResult(task_id)

        progress = redis_client.get(f"report:progress:{task_id}")
        progress = int(progress) if progress else 0

        return Response({
            "task_id": task_id,
            "status": result.status,
            "progress": progress,
            "result": result.result
        })


class CancelReportAPIView(APIView):
    """
    Covers:
    - task cancellation
    """

    def post(self, request, task_id):
        control = Control(app)
        control.revoke(task_id, terminate=True)

        return Response({
            "task_id": task_id,
            "message": "Task cancelled"
        })
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult

from .serializers import GenerateTextSerializer
from .tasks import run_ollama_prompt
'''
2️⃣ When @extend_schema is REQUIRED

You MUST use it when:

    Using @api_view (function-based views)
    Swagger doesn’t show parameters correctly
    You want explicit request/response contracts

Without it, Swagger often behaves inconsistently.


celery -A ST worker -l info --pool=solo
2️⃣ -A ST — Application / project reference
3️⃣ worker — start a worker process
4️⃣ -l info — logging level
5️⃣ --pool=solo — use solo pool for compatibility on Windows


django-celery-results - the results backend for storing task results in the database ,id generated when task is created
django-celery-beat - for periodic tasks scheduling
'''
class GenerateTextView(APIView):
    serializer_class = GenerateTextSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        prompt = serializer.validated_data["prompt"]
        model = serializer.validated_data.get("model", "deepseek-coder:6.7b")

        task = run_ollama_prompt.delay(prompt, model)

        return Response(
            {
                "task_id": task.id,
                "status": "processing"
            },
            status=status.HTTP_202_ACCEPTED
        )


class TaskStatusView(APIView):

    def get(self, request, task_id):
        result = AsyncResult(task_id)

        return Response({
            "task_id": task_id,
            "state": result.state,
            "result": result.result if result.successful() else None,
        })
