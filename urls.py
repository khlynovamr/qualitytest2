from django.urls import path
from . import views

app_name = 'quality_tests_app'

urlpatterns = [
    path('', views.choose_test_view, name='choose_test'),
    path('demo_tests/', views.choose_demo_test_view, name='choose_demo_test'),
    path('test<str:test>/question<int:num>/', views.question_view, name='question'),
    path('test<str:test>/finish/', views.finish_test_view, name='finish_test'),
    path('login/', views.login_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
]
