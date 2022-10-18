from rest_framework import serializers
from apps.users.models import AdminUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'last_login']
