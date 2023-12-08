from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import UserProfile, UserLanguageProficiency, Language


class UserProfileSerializer(serializers.ModelSerializer):
    native_language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), write_only=True)
    learning_language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), write_only=True)

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
            is_active=False
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



# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import UserProfile, UserLanguageProficiency
# from learning.models import UserWord, UserSentence, UserPracticeBuffer
# from languages.models import Language, Word, Sentence
#
#
# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Language
#         fields = ['id', 'name']
#
# class UserWordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserWord
#         fields = ['word', 'proficiency_level', 'last_practiced']
#
# class UserSentenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserSentence
#         fields = ['sentence', 'proficiency_level', 'last_practiced']
#
# class UserLanguageProficiencySerializer(serializers.ModelSerializer):
#     language = LanguageSerializer(read_only=True)
#     language_id = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), write_only=True, source='language')
#     class Meta:
#         model = UserLanguageProficiency
#         fields = ['language',
#                   'language_id',
#                   'proficiency_level',
#                   'proficiency_weights',
#                   'is_active',
#                   'buffer_size',
#                   'buffer_location',
#                   'buffer_range_start',
#                   'buffer_range_end']
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     native_language = LanguageSerializer(read_only=True)
#     native_language_id = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), write_only=True, source='native_language')
#     learning_languages = serializers.PrimaryKeyRelatedField(many=True, queryset=Language.objects.all())
#
#     class Meta:
#         model = UserProfile
#         fields = ['native_language', 'native_language_id', 'learning_languages']
#
#     def create(self, validated_data):
#         learning_languages_data = validated_data.pop('learning_languages', [])
#         user_profile = UserProfile.objects.create(**validated_data)
#
#         # This will handle the ManyToMany assignment correctly
#         if learning_languages_data:
#             learning_language_ids = [lang.id for lang in learning_languages_data]
#             learning_language_objects = Language.objects.filter(id__in=learning_language_ids)
#             user_profile.learning_languages.set(learning_language_objects)
#
#         return user_profile
#
#     # def create(self, validated_data):
#     #     learning_languages_data = validated_data.pop('learning_languages', [])
#     #     user_profile = UserProfile.objects.create(**validated_data)
#     #
#     #     learning_language_objects = Language.objects.filter(id__in=learning_languages_data)
#     #     user_profile.learning_languages.set(learning_language_objects)
#     #
#     #     # for language in learning_languages:
#     #     #     UserLanguageProficiency.objects.create(user_profile=user_profile, language=language)
#     #
#     #     return user_profile
#
#
# class UserSerializer(serializers.ModelSerializer):
#     userprofile = UserProfileSerializer()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'userprofile']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         userprofile_data = validated_data.pop('userprofile', {})
#         user = User.objects.create_user(**validated_data)
#         UserProfile.objects.create(user=user, **userprofile_data)
#
#         return user


# class UserProfileSerializer(serializers.ModelSerializer):
#     learning_languages = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Language.objects.all()
#     )
#     native_language = serializers.PrimaryKeyRelatedField(
#         queryset=Language.objects.all(), allow_null=True
#     )
#
#     class Meta:
#         model = UserProfile
#         fields = ['learning_languages', 'native_language']
#
#
# class NewUserSerializer(serializers.ModelSerializer):
#     userprofile = UserProfileSerializer(required=False)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'userprofile']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         userprofile_data = validated_data.pop('userprofile', {})
#         user = User.objects.create_user(**validated_data)
#
#         learning_languages = userprofile_data.get('learning_languages', [])
#         native_language = userprofile_data.get('native_language', None)
#
#         user_profile = UserProfile.objects.create(
#             user=user, native_language=native_language
#         )
#
#         for language in learning_languages:
#             UserLanguageProficiency.objects.create(
#                 user_profile=user_profile, language=language
#             )
#
#         return user


