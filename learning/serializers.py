from rest_framework import serializers
from languages.models import Language
from .models import UserWordBank

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('value',)

class SentencePairSerializer(serializers.Serializer):
    word = serializers.CharField()
    sentence = serializers.CharField()
    translation = serializers.CharField()
    sentence_language = serializers.CharField()
    translation_language = serializers.CharField()


class LearningViewResponseSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    learning_language = LanguageSerializer()  # Assuming LanguageSerializer is already defined
    native_language = LanguageSerializer()
    proficiency = serializers.FloatField()
    learned_word_count = serializers.IntegerField()
    buffer = SentencePairSerializer(many=True)  # List of sentence pairs


class UserWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWordBank
        fields = ['word_item', 'proficiency_level', 'last_practiced']

