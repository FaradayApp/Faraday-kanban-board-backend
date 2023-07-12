from rest_framework import serializers

from users.services import entries


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=33)
    first_name = serializers.CharField(max_length=32, required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=32, required=False, allow_null=True, allow_blank=True)
    avatar = serializers.CharField(max_length=32, required=False, allow_null=True, allow_blank=True)

    def to_entry(self) -> entries.UserEntry:
        return entries.UserEntry(
            **self.validated_data
        )


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=33)


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
