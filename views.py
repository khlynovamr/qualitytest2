from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from quality_tests_app import forms as app_forms
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required


@login_required(login_url="quality_tests_app:auth")
def choose_test_view(request):
    user_quality_tests = UserTestPassing.objects.filter(user=request.user).values_list('quality_test', flat=True)
    quality_tests = QualityTest.objects.exclude(is_demonstrate=True)
    quality_tests = quality_tests.exclude(id__in=user_quality_tests)
    for quality_test in quality_tests:
        questions_num = QualityTestQuestion.objects.filter(quality_test=quality_test).count()
        quality_test.questions_num = questions_num
    context = {
        'quality_tests': quality_tests,
    }
    return render(request, "choose_test.html", context)


@login_required(login_url="quality_tests_app:auth")
def choose_demo_test_view(request):
    demo_tests = QualityTest.objects.filter(is_demonstrate=True)
    for test in demo_tests:
        questions_num = QualityTestQuestion.objects.filter(quality_test=test).count()
        test.questions_num = questions_num
    context = {
        'demo_tests': demo_tests,
    }
    return render(request, "choose_demo_test.html", context)


@login_required(login_url="quality_tests_app:auth")
def question_view(request, test, num):
    quality_test = QualityTest.objects.get(pk=test)
    question_count = QualityTestQuestion.objects.filter(quality_test=test).count()
    if num == question_count + 1:
        is_last_question = True
    else:
        is_last_question = False
    if request.method == 'POST':
        prev_question = QualityTestQuestion.objects.filter(quality_test=test)[num - 2]
        right_answers = list(
            QualityTestQuestionAnswer.objects.filter(question=prev_question, is_right=True).values_list('id',
                                                                                                        flat=True))
        user_answers = list(map(int, request.POST.getlist("answer")))
        if len(user_answers) == 0:
            messages.error(request, "Вы не выбрали ни один из ответов!")
            return redirect('quality_tests_app:question', test, num - 1)
        else:
            if not quality_test.is_demonstrate:
                user_test_passing, created = UserTestPassing.objects.get_or_create(user=request.user, quality_test=quality_test)
                user_test_passing_answer, created = UserTestPassingAnswer.objects.get_or_create(test_passing=user_test_passing,
                                                                                                question=prev_question)
                for user_answer in user_answers:
                    user_test_passing_answer.answers.add(QualityTestQuestionAnswer.objects.get(pk=user_answer))
                if right_answers == user_answers:
                    user_test_passing_answer.is_answer_right = True
                else:
                    user_test_passing_answer.is_answer_right = False
                user_test_passing_answer.save()
                user_test_passing.save()
            if is_last_question:
                return redirect("quality_tests_app:finish_test", quality_test.id)
    try:
        # if not num > question_count:
        question = QualityTestQuestion.objects.filter(quality_test=test)[num - 1]
        answers = QualityTestQuestionAnswer.objects.filter(question=question)
        right_answers_num = answers.filter(is_right=True).count()
        if right_answers_num > 1:
            multiple_answers = True
        else:
            multiple_answers = False
        new_num = num + 1
        context = {
            'question': question,
            'answers': answers,
            'test': test,
            'num': num,
            'new_num': new_num,
            'multiple_answers': multiple_answers,
            'is_last_question': is_last_question,
        }
    except:
        context = {
            'message': "Нет такой страницы!",
        }
        return render(request, "message.html", context)
    return render(request, "question.html", context)


@login_required(login_url="quality_tests_app:auth")
def finish_test_view(request, test):
    quality_test = QualityTest.objects.get(pk=test)
    if quality_test.is_demonstrate:
        message = "Спасибо за прохождение!"
    else:
        message = "Спасибо за прохождение! Узнать результаты вы сможете у руководителя!"
    context = {
        'message': message,
    }
    return render(request, "message.html", context)


def login_view(request):
    login_form = app_forms.AuthForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('quality_tests_app:choose_test')
    context = {
        'input_form': login_form,
    }
    return render(request, "auth.html", context)


def logout_view(request):
    logout(request)
    return redirect("quality_tests_app:choose_test")


def about_view(request):
    return render(request, "about.html")
