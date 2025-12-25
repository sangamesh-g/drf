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

class RegisterView(APIView):
    permission_classes=[]

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