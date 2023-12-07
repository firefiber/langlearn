from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserLanguageProficiency
from languages.models import Language


class UserProfileSerializer(serializers.ModelSerializer):
    learning_languages = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Language.objects.all()
    )
    native_language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), allow_null=True
    )

    class Meta:
        model = UserProfile
        fields = ['learning_languages', 'native_language']


class NewUserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'userprofile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile', {})
        user = User.objects.create_user(**validated_data)

        learning_languages = userprofile_data.get('learning_languages', [])
        native_language = userprofile_data.get('native_language', None)

        user_profile = UserProfile.objects.create(
            user=user, native_language=native_language
        )

        for language in learning_languages:
            UserLanguageProficiency.objects.create(
                user_profile=user_profile, language=language
            )

        return user


