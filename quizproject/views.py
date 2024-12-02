from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Quiz, Question, Answer, UserStat
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, UserStatSerializer,SubmitQuizserializer
from django.utils.timezone import now
from datetime import timedelta

#view to fetch the quiz list
class QuizListAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.all()  # Retrieve all quizzes
        serializer = QuizSerializer(quizzes, many=True)  # Serialize the quiz data
        return Response(serializer.data, status=status.HTTP_200_OK)

#view to fetch the quizdetail data
class QuizDetailAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = Question.objects.filter(quiz=quiz).prefetch_related('answers')
        quiz_data = QuizSerializer(quiz).data

        #add questions and answers to the response
        quiz_data['questions'] = []
        for question in questions:
            question_data = QuestionSerializer(question).data
            answers = question.answers.all()
            question_data['answers']=AnswerSerializer(answers,many=True).data
            quiz_data['questions'].append(question_data)
        
        return Response(quiz_data, status=status.HTTP_200_OK)
    
#view to submit answers for evaluation
class SubmitQuizApiView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, quiz_id):
        print("Request data:", request.data)
        quiz = get_object_or_404(Quiz, id=quiz_id)
        user = request.user 
        
        serializer = SubmitQuizserializer(data=request.data,context={"quiz_id": quiz_id})
        if serializer.is_valid():
            submitted_data = serializer.validate_answers(request.data['answers'])
            score = 0
            correct_answers = 0
            total_questions = Question.objects.filter(quiz=quiz).count()

            for item in submitted_data:
                question_id = item['question']  # Access the question ID
                selected_answer = item['answer'] 
                question = get_object_or_404(Question, id=question_id,quiz=quiz)
                correct_answer_ids = set(Answer.objects.filter(question=question, is_correct=True).values_list("id", flat=True))

                # Handle multiple answers
                if isinstance(selected_answer, list):
                    if set(selected_answer) == correct_answer_ids:
                        score += 1
                        correct_answers += 1
                else:  # Single answer
                    if {selected_answer} == correct_answer_ids:
                        score += 1
                        correct_answers += 1
        
            #save user statisctics
            UserStat.objects.create(
                user=user,
                quiz=quiz,
                score=score,
                time_taken=timedelta(minutes=5),
                date_taken=now()
            )

            return Response({
                'message': 'Quiz submitted Successfully',
                'score': score,
                'correct_answers':correct_answers,
                'total_questions':total_questions,
            }, status=status.HTTP_200_OK) 
    
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#view to retrieve the user stat
class UserStatisticsView(APIView):
    def get(self, request):
        user = request.user
        stats = UserStat.objects.filter(user=user)
        serializer = UserStatSerializer(stats, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)