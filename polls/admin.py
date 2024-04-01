from django.contrib import admin
from . import models

class ChoiceInline(admin.TabularInline):
    model = models.Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('publication Date',{'fields': ['pub_date']}),
    ]

    inlines = [ChoiceInline]


admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Choice)
