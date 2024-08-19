from django.db import models
from src.users.models import User


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_lesson_done = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f'{self.user.username} - {self.lesson.title} - {self.progress}%'


class Test(models.Model):
    question = models.CharField(max_length=500)
    answer1 = models.CharField(max_length=200)
    answer2 = models.CharField(max_length=200)
    answer3 = models.CharField(max_length=200)
    answer4 = models.CharField(max_length=200, blank=True, null=True)
    answer5 = models.CharField(max_length=200, blank=True, null=True)
    correct_answer = models.IntegerField()

    def __str__(self):
        return self.question


class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    selected_answer = models.IntegerField()
    is_answer_correct = models.BooleanField()

    class Meta:
        unique_together = ['user', 'test']

    def __str__(self):
        return f'{self.user.username} - {self.test.question} - {"Correct" if self.is_answer_correct else "Incorrect"}'



class Broker(models.Model):
    broker_name = models.CharField(max_length=200)
    min_deposit = models.IntegerField()
    link = models.URLField(max_length=200)
    broker_image = models.URLField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.broker_name

# models.py
class BrokerInfo(models.Model):
    info = models.TextField()

    def __str__(self):
        return "Broker Information"
