from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name',
                  'last_name', 'phone_number', 'password', 'role')

    def create(self, validated_data):
        # Используем наш кастомный менеджер для создания хешированного пароля
        user = User.objects.create_user(**validated_data)
        return user
