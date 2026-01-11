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