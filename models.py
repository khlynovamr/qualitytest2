from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class QualityTestTopic(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название темы')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тема тестов'
        verbose_name_plural = 'Темы для тестов'


class QualityTest(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название')
    topic = models.ForeignKey(QualityTestTopic, on_delete=models.CASCADE, verbose_name='Тема')
    description = models.CharField(max_length=400, null=True, blank=True, verbose_name="Краткое описание теста")
    is_demonstrate = models.BooleanField(verbose_name="Демонстрационный тест", default=False)

    def __str__(self):
        return f'{self.name} [{self.topic}]'

    class Meta:
        verbose_name = 'Квалификационный тест'
        verbose_name_plural = 'Квалификационные тесты'
        ordering = ['name']


class QualityTestQuestion(models.Model):
    quality_test = models.ForeignKey(QualityTest, on_delete=models.CASCADE, verbose_name='Тест')
    question_text = models.TextField(verbose_name='Текст вопроса', max_length=1000)
    is_many_variants = models.BooleanField(verbose_name="Может содержать несколько правильных ответов", default=True)

    def __str__(self):
        return f'{self.quality_test} id вопроса: {self.id}'

    class Meta:
        verbose_name = 'Вопрос в тесте'
        verbose_name_plural = 'Вопросы в тесте'
        ordering = ['id']


class QualityTestQuestionAnswer(models.Model):
    question = models.ForeignKey(QualityTestQuestion, on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.TextField(verbose_name='Текст ответа', max_length=250)
    is_right = models.BooleanField(default=False, verbose_name="Верный ответ")

    def __str__(self):
        return f'Тест: {self.question.quality_test} Номер вопроса:{self.question.id}, {self.text}'

    class Meta:
        verbose_name = 'Ответ на вопрос в тесте'
        verbose_name_plural = 'Ответы на вопросы в тестах'
        ordering = ['question']


class UserTestPassing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    quality_test = models.ForeignKey(QualityTest, on_delete=models.CASCADE, verbose_name="Тест")
    date_time = models.DateTimeField(verbose_name="Дата и время сохранения результатов теста", default=datetime.now)
    test_questions_num = models.IntegerField(default=0, verbose_name="Число вопросов в тесте")
    right_answers_num = models.IntegerField(default=0, verbose_name="Число верных ответов пользователя")
    pass_percent = models.FloatField(default=0, verbose_name="Процент прохождения теста")

    def __str__(self):
        return f'{self.user} [{self.quality_test.name}]'

    def save(self, *args, **kwargs):
        if not self._state.adding:
            user_answers = UserTestPassingAnswer.objects.filter(test_passing=self)
            test_questions = QualityTestQuestion.objects.filter(quality_test=self.quality_test)
            right_answers_num = 0
            for answer in user_answers:
                if answer.is_answer_right:
                    right_answers_num += 1
            self.right_answers_num = right_answers_num
            self.test_questions_num = test_questions.count()
            self.pass_percent = round(right_answers_num / self.test_questions_num * 100, 2)
        super(UserTestPassing, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Прохождение теста'
        verbose_name_plural = 'Прохождения тестов'
        ordering = ['quality_test', 'user']


class UserTestPassingAnswer(models.Model):
    test_passing = models.ForeignKey(UserTestPassing, on_delete=models.CASCADE, verbose_name="Прохождение теста")
    question = models.ForeignKey(QualityTestQuestion, on_delete=models.CASCADE, verbose_name="Вопрос теста")
    answers = models.ManyToManyField(QualityTestQuestionAnswer, verbose_name="Ответ пользователя", null=True, blank=True)
    is_answer_right = models.BooleanField(verbose_name="Ответ верный", default=False)

    def __str__(self):
        return f'{self.test_passing.quality_test.name} {self.test_passing.user} [id: {self.question.id}]'

    class Meta:
        verbose_name = 'Ответ прохождения'
        verbose_name_plural = 'Ответы в прохождениях тестов'
        ordering = ['question', 'test_passing']
