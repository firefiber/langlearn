from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import UserProfile, UserLanguageProficiency, Language


class UserProfileSerializer(serializers.ModelSerializer):
    native_language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.filter(category__in=['N', 'B']), write_only=True)
    learning_language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.filter(category__in=['L', 'B']), write_only=True)

    class Meta:
        model = UserProfile
        fields = ['native_language', 'learning_language_id']

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'userprofile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        native_language = userprofile_data.pop('native_language')
        learning_language_id = userprofile_data.pop('learning_language_id', None)

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            is_active=True
        )
        user.save()

        user_profile = UserProfile.objects.create(
            user=user, native_language=native_language
        )

        if learning_language_id:
            UserLanguageProficiency.objects.create(
                user_profile=user_profile,
                language=learning_language_id,
                is_active=True
            )

        return user