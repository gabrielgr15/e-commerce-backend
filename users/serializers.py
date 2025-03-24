from .models import CustomUser
from rest_framework.serializers import ModelSerializer

class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
