from rest_framework import serializers
from .models import Lesson, LessonProgress, TestAttempt, Test, Broker, BrokerInfo


class LessonSerializer(serializers.ModelSerializer):
    is_done = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'is_done', 'order']

    def get_is_done(self, obj):
        user = self.context['request'].user
        lesson_progress = LessonProgress.objects.filter(user=user, lesson=obj).first()
        return lesson_progress is not None and lesson_progress.is_lesson_done is True


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['user', 'lesson', 'is_lesson_done']


class TestSerializer(serializers.ModelSerializer):
    is_answer_correct = serializers.SerializerMethodField()
    class Meta:
        model = Test
        fields = ['id', 'question', 'answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'correct_answer',
                  'is_answer_correct']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key in representation.keys():
            if representation[key] is None:
                representation[key] = ''
        return representation

    def get_is_answer_correct(self, obj):
        user = self.context['request'].user
        test_attempt = TestAttempt.objects.filter(user=user, test=obj).first()
        return test_attempt is not None and test_attempt.is_answer_correct is True


class TestAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAttempt
        fields = ['user', 'test', 'selected_answer', 'is_answer_correct']


class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = ['broker_name', 'min_deposit', 'link', 'broker_image', 'description']


# serializers.py
class BrokerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerInfo
        fields = ['info']
