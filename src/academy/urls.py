from rest_framework.routers import SimpleRouter
from src.academy.views import LessonViewSet, LessonProgressViewSet, TestAttemptViewSet, TestViewSet, BrokerViewSet

academy_router = SimpleRouter()
academy_router.register(r'lessons', LessonViewSet)
academy_router.register(r'tests', TestViewSet, basename='tests')
academy_router.register(r'lesson-progress', LessonProgressViewSet, basename='lesson-progress')
academy_router.register(r'test-attempt', TestAttemptViewSet, basename='test-attempt')
academy_router.register(r'brokers', BrokerViewSet)
