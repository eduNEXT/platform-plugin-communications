from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSearchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="profile.name", read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "name",
        )
