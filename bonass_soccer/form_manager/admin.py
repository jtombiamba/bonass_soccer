from django.contrib import admin
from django.contrib.admin import ModelAdmin
from bonass_soccer.form_manager.models.conditions import ConditionClause, Condition
from bonass_soccer.form_manager.models.models import BaseForm, Question, Page, Choice
from bonass_soccer.form_manager.models.responses import FormResponse, Answer
from nested_admin.nested import NestedTabularInline, NestedModelAdmin



class QuestionInline(NestedTabularInline):
    model = Question
    extra = 1

class PageInline(NestedTabularInline):
    model = Page
    extra = 1
    inlines = [QuestionInline]  # Nest QuestionInline inside PageInline

@admin.register(BaseForm)
class FormAdmin(NestedModelAdmin):
    inlines = [PageInline]
    # prepopulated_fields = {"slug": ("title",)}
    list_display = ["id", "title", "description"]



# # Register your models here.
# class BaseFormAdmin(ModelAdmin):
#     list_display = ["id", "title"]
#     fields = ["title", "description"]
#
#
class PageAdmin(ModelAdmin):
    list_display = ["id", "order", "form", "title"]
    fields = ["form", "title"]


class QuestionAdmin(ModelAdmin):
    list_display = ["id", "order", "page", "answer_type", "text", "required"]
    fields = ["page", "answer_type", "text", "required"]

class ConditionAdmin(ModelAdmin):
    list_display = ["id", "target_question"]
    fields = ["target_question"]


# class ConditionClauseAdmin(ModelAdmin):
#     list_display = ["id"]
#     fields = ["pace", "assist", "defense", "shoot", "dribble"]


class ChoiceAdmin(ModelAdmin):
    list_display = ["id"]
    fields = ["pace", "assist", "defense", "shoot", "dribble"]

class FormResponseAdmin(ModelAdmin):
    list_display = ["id", "form"]

class AnswerAdmin(ModelAdmin):
    list_display = ["id", "response", "question"]



# admin.site.register(BaseForm, BaseFormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Condition, ConditionAdmin)
# admin.site.register(ConditionClause, ConditionClauseAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(FormResponse, FormResponseAdmin)
admin.site.register(Answer, AnswerAdmin)