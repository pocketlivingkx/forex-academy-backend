from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from src.users.permissions import IsUserOrReadOnly

from .models import Lesson, LessonProgress, TestAttempt, Test, Broker, BrokerInfo
from .serializers import (LessonSerializer, LessonProgressSerializer, TestAttemptSerializer, TestSerializer,
                          BrokerSerializer, BrokerInfoSerializer)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        user_id = self.request.user.id
        only_unresolved_tests = request.query_params.get('only_unresolved_tests', 'false') == 'true'
        tests_amount = int(request.query_params.get('tests_amount', '0'))

        # Get all the tests
        tests = Test.objects.all()

        if only_unresolved_tests:
            # Get the tests that the user has solved
            solved_tests = TestAttempt.objects.filter(user_id=user_id, is_answer_correct=True).values_list('test_id',
                                                                                                           flat=True)
            # Exclude the solved tests
            tests = tests.exclude(id__in=solved_tests)

        # Order the tests in random order
        tests = tests.order_by('?')

        if tests_amount > 0:
            # Limit the number of tests returned
            tests = tests[:tests_amount]

        serializer = TestSerializer(tests, many=True, context={'request': request})
        return Response(serializer.data)


class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Lesson.objects.all()

class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_queryset(self):
        user_id = self.request.user.id
        return LessonProgress.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        lesson_id = request.data.get('lesson_id')
        is_lesson_done = request.data.get('is_lesson_done', 'false') == 'true'

        if not lesson_id:
            return Response({'error': 'lesson_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        lesson_progress, created = LessonProgress.objects.get_or_create(
            user_id=user_id,
            lesson_id=lesson_id,
            defaults={'is_lesson_done': is_lesson_done},
        )

        response_status = status.HTTP_200_OK
        if not created:
            lesson_progress.is_lesson_done = is_lesson_done
            lesson_progress.save()
            response_status = status.HTTP_201_CREATED

        serializer = self.get_serializer(lesson_progress)
        return Response(serializer.data, status=response_status)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_lesson_done = request.data.get('is_lesson_done', instance.is_lesson_done)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TestAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = TestAttemptSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_queryset(self):
        user_id = self.request.user.id
        return TestAttempt.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        test_id = request.data.get('test_id')
        user_answer = request.data.get('user_answer')

        if user_answer not in ('0', '1', '2', '3', '4', '5'):
            return Response({'error': 'user_answer can be from 1 to 5'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not test_id:
            return Response({'error': 'test_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the test instance
        test = Test.objects.get(id=test_id)

        # Check if the user's answer is correct
        is_answer_correct = test.correct_answer == int(user_answer)

        test_attempt, created = TestAttempt.objects.get_or_create(
            user_id=user_id,
            test_id=test_id,
            defaults={'selected_answer': user_answer, 'is_answer_correct': is_answer_correct},
        )

        response_status = status.HTTP_200_OK
        if not created:
            test_attempt.selected_answer = user_answer
            test_attempt.is_answer_correct = is_answer_correct
            test_attempt.save()
            response_status = status.HTTP_201_CREATED

        serializer = self.get_serializer(test_attempt)

        return Response(serializer.data, status=response_status)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.selected_answer = request.data.get('selected_answer', instance.selected_answer)
        instance.is_answer_correct = request.data.get('is_answer_correct', instance.is_answer_correct)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BrokerViewSet(viewsets.ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        broker_info = BrokerInfo.objects.first()
        broker_info_serializer = BrokerInfoSerializer(broker_info)

        # Add the broker information to the response
        return Response({
            'data': serializer.data,
            'broker_info': broker_info_serializer.data,
        })
