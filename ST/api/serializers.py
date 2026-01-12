from employees.models import Employee
from rest_framework import serializers
from .models import profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=profile
        fields=["id", "fullname"]
    


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    fullname = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already exists")
        return value
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        return value
    
    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        profile.objects.create(
            user=user,
            fullname=validated_data['fullname']
        )
        return user
    
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class LoginSerializer(TokenObtainPairSerializer):

    def validate(self,attrs):
        data=super().validate(attrs)

        data["user"]={
            "username":self.user.username,
            "email":self.user.email,
        }
        return data


class GenerateTextSerializer(serializers.Serializer):
    prompt = serializers.CharField(
        max_length=5000,
        help_text="Prompt sent to the LLM"
    )
    model = serializers.CharField(
        required=False,
        default="deepseek-coder:6.7b"
    )
