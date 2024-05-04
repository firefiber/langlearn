from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from learning.models import UserWordBank
from .models import UserProfile, UserLanguageProficiency
from languages.models import Language, Word
from datetime import datetime, timedelta

class LearningLanguageSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source='language.value')

    class Meta:
        model = UserLanguageProficiency
        fields = ['language_name', 'is_active']

class UserDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    native_language = serializers.CharField(source='native_language.value')
    learning_languages = serializers.SerializerMethodField()
    learning_since = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'native_language', 'learning_languages', 'learning_since']

    def get_learning_languages(self, obj):
        # Get learning languages with their 'is_active' status
        learning_languages = {prof.language.value: prof.is_active for prof in obj.userlanguageproficiency_set.all()}
        return learning_languages

    def get_learning_since(self, obj):
        return obj.user.date_joined.strftime("%Y-%m-%d") if obj.user.date_joined else None

class UserTrainingDataSerializer(serializers.ModelSerializer):
    proficiency = serializers.FloatField(source='proficiency_level')
    word_bank_count = serializers.SerializerMethodField()
    streak = serializers.SerializerMethodField()

    class Meta:
        model = UserLanguageProficiency
        fields = ['proficiency', 'word_bank_count', 'streak']

    def get_word_bank_count(self, obj):
        # Fetch all UserWord instances for the user
        user_words = UserWordBank.objects.filter(user_profile=obj.user_profile)
        # Fetch all Word instances for the active language
        words_in_language = Word.objects.filter(language=obj.language).values_list('value', flat=True)

        # Count how many user words are in the words of the active language
        word_bank_count = sum(1 for user_word in user_words if user_word.value in words_in_language)

        return word_bank_count
    def get_streak(self, obj):
        # Logic to calculate the streak goes here
        # This is a placeholder logic, modify it according to your actual streak calculation
        today = datetime.now().date()
        streak = 0
        for i in range(30):  # Check the last 30 days as an example
            if UserWordBank.objects.filter(user_profile=obj.user_profile, last_practiced__date=today - timedelta(days=i)).exists():
                streak += 1
            else:
                break
        return streak

class UserProfileSerializer(serializers.ModelSerializer):
    native_language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.filter(category__in=['N', 'B']), write_only=True)
    learning_language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.filter(category__in=['L', 'B']), write_only=True)

    class Meta:
        model = UserProfile
        fields = ['native_language', 'learning_language_id']

class UserRegistrationSerializer(serializers.ModelSerializer):
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