from django.contrib import admin
from .models import Quiz, Question, Answer, UserStat

# Register the Quiz model with the admin interface
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','created_on')  # Display these fields in the admin list view

admin.site.register(Quiz, QuizAdmin)


# Register the Question model with the admin interface
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'questions', 'created_on')  # Display these fields in the admin list view

admin.site.register(Question, QuestionAdmin)


# Register the Answer model with the admin interface
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'is_correct','answer_type','created_on')  # Display these fields in the admin list view

admin.site.register(Answer, AnswerAdmin)


# Register the UserStat model with the admin interface
class UserStatAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'time_taken','date_taken')  # Display these fields in the admin list view

admin.site.register(UserStat, UserStatAdmin)
