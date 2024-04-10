from django.contrib import admin
from django import forms

from .models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

admin.site.site_header = "Управление квалификационными тестами"


class QualityTestInline(admin.StackedInline):
    model = QualityTest
    show_change_link = True
    extra = 0


class QualityTestQuestionInline(admin.StackedInline):
    model = QualityTestQuestion
    show_change_link = True
    extra = 0


class QualityTestQuestionAnswerInline(admin.StackedInline):
    model = QualityTestQuestionAnswer
    show_change_link = True
    extra = 0


class UserTestPassingInline(admin.StackedInline):
    model = UserTestPassing
    show_change_link = True
    extra = 0


class UserTestPassingAnswerInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['answer'].queryset = QualityTestQuestionAnswer.objects.filter(question=self.instance.question)
        except:
            pass


class UserTestPassingAnswerInline(admin.StackedInline):
    model = UserTestPassingAnswer
    show_change_link = True
    extra = 0
    form = UserTestPassingAnswerInlineForm

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'question':
            parent_id = request.resolver_match.kwargs.get('object_id')
            user_test_passing = UserTestPassing.objects.get(id=parent_id)
            kwargs['queryset'] = QualityTestQuestion.objects.filter(quality_test=user_test_passing.quality_test)
        return super(UserTestPassingAnswerInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "answers":
            parent_id = request.resolver_match.kwargs.get('object_id')
            user_test_passing = UserTestPassing.objects.get(id=parent_id)
            quality_test_questions = QualityTestQuestion.objects.filter(quality_test=user_test_passing.quality_test)
            kwargs['queryset'] = QualityTestQuestionAnswer.objects.filter(question__in=quality_test_questions)
        return super(UserTestPassingAnswerInline, self).formfield_for_manytomany(db_field, request, **kwargs)


class QualityTestTopicAdmin(admin.ModelAdmin):
    inlines = [QualityTestInline]
    list_display = [
        'name',
    ]


class QualityTestAdmin(admin.ModelAdmin):
    inlines = [QualityTestQuestionInline]
    list_display = [
        'name',
        'topic',
        'is_demonstrate',
    ]


class QualityTestQuestionAdmin(admin.ModelAdmin):
    inlines = [QualityTestQuestionAnswerInline]


class UserTestPassingAdmin(admin.ModelAdmin):
    inlines = [UserTestPassingAnswerInline]
    list_display = [
        'quality_test',
        'user',
        'date_time',
        'test_questions_num',
        'right_answers_num',
        'pass_percent',
    ]

    def save_model(self, request, obj, form, change):
        pass

    def save_formset(self, request, form, formset, change):
        formset.save()
        form.instance.save()


class UserAdmin(DjangoUserAdmin):
    inlines = [UserTestPassingInline]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name',)}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = [
        'username',
        'first_name',
        'email',
        'is_staff',
        'is_active',
    ]


admin.site.register(QualityTestTopic, QualityTestTopicAdmin)
admin.site.register(QualityTest, QualityTestAdmin)
admin.site.register(QualityTestQuestion, QualityTestQuestionAdmin)
admin.site.register(QualityTestQuestionAnswer)
admin.site.register(UserTestPassing, UserTestPassingAdmin)
admin.site.register(UserTestPassingAnswer)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
