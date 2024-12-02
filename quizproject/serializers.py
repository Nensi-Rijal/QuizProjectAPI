from rest_framework import serializers
from .models import Quiz, Question, Answer, UserStat

#Quiz_Serializers
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_on']

    #validation to ensure title is not blank and holds some meaning
    def validate_title(self,value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Title cannot be empty")
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value
    
#Question_Serializers
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'questions', 'created_on']

        def validate_questions(self,value):
            if len(value.strip()) == 0:
                raise serializers.ValidationError("Question text cannot be empty")
            if len(value) < 10:
                raise serializers.ValidationError("Question must be at least 10 characters long")
            return value
        
        def validate_quiz(self,value):
            #validation to ensure that the quiz exists
            if not Quiz.objects.filter(id=value.id).exists():
                raise serializers.ValidationError("The provided quiz does not exist")
            return value

#Answer_Serializers
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer', 'is_correct','answer_type','created_on']
    
    #validation to ensure any one answer exists for a question
    def validate(self, data):
        question = data.get('question')
        is_correct = data.get('is_correct')

        if is_correct:
            existing_correct_answers = Answer.objects.filter(question = question, is_correct=True).count()
            if existing_correct_answers >= 1:
                raise serializers.ValidationError("Each question can only have one correct answer for single type answer")
            
        #validation for other 
        if len(data.get('answer').strip()) == 0:
            raise serializers.ValidationError("Answer text cannot be empty")
        
        return data
    
#User_Stat Serializers
class UserStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStat
        fields = ['id','user','quiz','score','time_taken','date_taken']

    def validate_score(self,value):
        if value < 0:
            raise serializers.ValidationError("Score cannot be negative")
        return value
    
    def validate_user(self,value):
        if not value.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to submit stats")
        return value
    
    def validate_quiz(self,value):
        if not Quiz.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("The provided quiz does not exist")
        return value
    

#submitquizserialier
class SubmitQuizserializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField()  # To allow flexibility for both single and multiple answers
        )
    )
    
    def validate_answers(self,value):
        if not value:
            raise serializers.ValidationError("No answers submitted")
        
        quiz_id = self.context.get('quiz_id')  # pass quiz_id in the context
        if not quiz_id:
            raise serializers.ValidationError("Quiz ID is missing from context.")
        questions = Question.objects.filter(quiz_id=quiz_id)
        answered_question_ids = {answer['question'] for answer in value}  # Collect question IDs from answers
        question_ids = {q.id for q in questions}  # Collect all question IDs in the quiz
    
        if not question_ids.issubset(answered_question_ids):
            raise serializers.ValidationError("Not all questions have been answered.")
        
        # Check answer types: single vs multiple
        for answer in value:
            question = questions.get(id=answer['question'])
            if question:
                # Check if the question expects multiple answers
                is_multiple = any(a.answer_type == 'multiple' for a in question.answers.all())

                # If the question is for multiple answers
                if is_multiple:
                    # Validate if it's a list of integers for multiple answers
                    if not isinstance(answer['answer'], list):
                        raise serializers.ValidationError(f"Question {answer['question']} expects multiple answers (list).")
                    if not all(isinstance(a, int) for a in answer['answer']):
                        raise serializers.ValidationError(f"Question {answer['question']} answers must be a list of integers.")
                    if len(answer['answer']) < 1:
                        raise serializers.ValidationError(f"Question {answer['question']} requires at least one answer.")

                # If the question is for a single answer
                else:
                    # Validate if it's a single integer for a single answer
                    if isinstance(answer['answer'], list):
                        raise serializers.ValidationError(f"Question {answer['question']} expects a single answer, not a list.")
                    if not isinstance(answer['answer'], int):  # Answer should be an integer (the ID)
                        raise serializers.ValidationError(f"Question {answer['question']} expects an integer answer.")
        return value