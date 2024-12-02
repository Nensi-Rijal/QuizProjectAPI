from django.db import models
from django.contrib.auth.models import User

#Quiz_Model
class Quiz(models.Model):
    title = models.CharField(max_length=255)    #Title of the quiz
    description = models.CharField(max_length=255,blank=True)  #Descriprion of the quiz, can be blank
    created_on = models.DateTimeField(auto_now_add=True)    # Date to be automatically set when created

    def __str__(self):
        return self.title


#Question_Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE) #each question belong to a quiz
    questions = models.TextField() #textfield for the questions text
    created_on = models.DateTimeField(auto_now_add=True) #Automatically set when the question was created

    def __str__(self):
        return f"{self.quiz.title:} {self.questions}"
    
#Answer_model
class Answer(models.Model):
    #Defining the three answer types
    SINGLE_ANSWER = 'single'
    MULTIPLE_ANSWER = 'multiple'
    SELECT_WORD = 'select_word'

    ANSWER_CHOICES = [
        (SINGLE_ANSWER, 'Single Answer'),
        (MULTIPLE_ANSWER, 'Multiple Answer'),
        (SELECT_WORD, 'Select a Word'),
    ]

    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answers')
    answer = models.CharField(max_length=255) #answer text
    is_correct = models.BooleanField(default=False) #initialized to false
    answer_type = models.CharField(
        max_length=20,
        choices=ANSWER_CHOICES,
        default=SINGLE_ANSWER, #default is set for the single answer option
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.answer} (correct: {self.is_correct}, Type: {self.answer_type})"
    
class UserStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField() #storing the users score
    time_taken = models.DurationField() #time taken by the user to complete the quiz
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} (score: {self.score})"