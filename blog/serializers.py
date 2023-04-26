from rest_framework import serializers
from blog.models import BlogPost

# model
from blog.models import User

# Authentication

# - Register
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Password and Confirm password do not match.')
        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

# - Login



# Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'created', 'last_updated']