from django.contrib import admin
from .models import Question, Choice
# Register your models here.


class ChoiceInline(admin.TabularInline):  # we can change the format of the
    # choice display
    """for the multiple choices."""
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    """customize the question model's field. display pub_date first rather than
     default field display."""
    # fields = ['pub_date', 'question_text']  # customize the field display
    # position here, pub_date display before question_text
    fieldsets = [
        ('Question Information', {'fields': ['question_text'], 'classes':['collapse']}),
        ('Date Information', {'fields': ['pub_date'], 'classes':['collapse']})
    ]  # use the add the field label in header format.
    inlines = [ChoiceInline]  # define inline choice filed here for the
    # multiple choices.
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']  # for the filter
    search_fields = ['question_text']  # for the search


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)