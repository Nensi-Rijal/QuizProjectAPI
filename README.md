# views.py

This module contains the API views for the quiz application. It uses Django REST framework to handle HTTP requests and responses. The views are protected with Basic Authentication and require the user to be authenticated.

## Classes

### QuizListAPIView
Handles the retrieval of the list of quizzes.

- **Methods:**
  - `get(self, request)`: Retrieves all quizzes and returns them as a serialized JSON response.

### QuizDetailAPIView
Handles the retrieval of detailed information about a specific quiz.

- **Methods:**
  - `get(self, request, quiz_id)`: Retrieves a specific quiz by its ID, along with its associated questions and answers, and returns them as a serialized JSON response.

## Imports

- `BasicAuthentication`: Provides basic HTTP authentication.
- `IsAuthenticated`: Ensures the user is authenticated.
- `APIView`: Base class for all API views.
- `Response`: Used to create HTTP responses.
- `status`: Contains HTTP status codes.
- `get_object_or_404`: Retrieves an object or returns a 404 error if not found.
- `Quiz, Question, Answer, UserStat`: Models representing the quiz, questions, answers, and user statistics.
- `QuizSerializer, QuestionSerializer, AnswerSerializer, UserStatSerializer, SubmitQuizSerializer`: Serializers for the models.
- `now`: Returns the current date and time.
- `timedelta`: Represents a duration, the difference between two dates or times.

## Usage

To use these views, include them in your Django project's URL configuration. Ensure that the user is authenticated to access these endpoints.

Example URL configuration:

```python
from django.urls import path
from .views import QuizListAPIView, QuizDetailAPIView

urlpatterns = [
    path('quizzes/', QuizListAPIView.as_view(), name='quiz-list'),
    path('quizzes/<int:quiz_id>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
]

# urls.py

This module defines the URL configuration for the `quizproject` Django project. It maps URL paths to the corresponding views, enabling the routing of HTTP requests to the appropriate handlers.

## URL Patterns

The `urlpatterns` list routes URLs to views. Below is a description of each URL pattern defined in this file:

- `admin/`: Routes to the Django admin interface.
- `quizzes/`: Routes to the `QuizListAPIView` view, which handles the retrieval of the list of quizzes.
- `quizzes/<int:quiz_id>/`: Routes to the `QuizDetailAPIView` view, which handles the retrieval of detailed information about a specific quiz.
- `quizzes/<int:quiz_id>/submit/`: Routes to the `SubmitQuizApiView` view, which handles the submission of quiz answers.
- `user-statistics/`: Routes to the `UserStatisticsView` view, which handles the retrieval of user statistics.

## Imports

- `admin`: The Django admin site module.
- `path`, `include`: Functions from `django.urls` used to define URL patterns.
- `QuizListAPIView`, `QuizDetailAPIView`, `SubmitQuizApiView`, `UserStatisticsView`: Views from the `views` module that handle the corresponding URL patterns.

## Usage

To use these URL patterns, include them in your Django project's main URL configuration. This file should be placed in the root directory of your Django app.

Example main URL configuration:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quizproject.urls')),
]


# serializers.py

This module defines the serializers for the quiz application. Serializers are used to convert complex data types, such as querysets and model instances, into native Python datatypes that can then be easily rendered into JSON, XML, or other content types. They also provide deserialization, allowing parsed data to be converted back into complex types.

## Classes and Methods

### SubmitQuizSerializer
Handles the serialization and validation of quiz submissions.

- **Fields:**
  - `answers`: A list of dictionaries, each containing the answers to the quiz questions. Each dictionary can contain single or multiple answers.

- **Methods:**
  - `validate_answers(self, value)`: Validates the submitted answers. Ensures that all questions have been answered and that the answers are in the correct format.

### Methods

#### validate_quiz(self, value)
Validates that the provided quiz exists.

- **Parameters:**
  - `value`: The quiz instance to validate.

- **Raises:**
  - `serializers.ValidationError`: If the quiz does not exist.

- **Returns:**
  - `value`: The validated quiz instance.

## Imports

- `serializers`: The Django REST framework serializers module.
- `Quiz`, `Question`: Models representing the quiz and questions.

## Usage

To use these serializers, include them in your views to handle the serialization and validation of data. Below is an example of how to use the `SubmitQuizSerializer` in a view:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SubmitQuizSerializer

class SubmitQuizApiView(APIView):
    def post(self, request, quiz_id):
        serializer = SubmitQuizSerializer(data=request.data, context={'quiz_id': quiz_id})
        if serializer.is_valid():
            # Process the valid data
            return Response({"message": "Quiz submitted successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# models.py

This module defines the database models for the quiz application. These models represent the structure of the database tables and define the relationships between different entities in the application.

## Models

### Quiz
Represents a quiz.

- **Fields:**
  - `title`: A `CharField` representing the title of the quiz.
  - `description`: A `CharField` representing the description of the quiz. This field is optional and can be blank.
  - `created_on`: A `DateTimeField` that is automatically set to the current date and time when the quiz is created.

- **Methods:**
  - `__str__(self)`: Returns the title of the quiz.

### Question
Represents a question in a quiz.

- **Fields:**
  - `quiz`: A `ForeignKey` to the `Quiz` model, indicating that each question belongs to a specific quiz. If the quiz is deleted, the associated questions are also deleted.
  - `questions`: A `TextField` representing the text of the question.
  - `created_on`: A `DateTimeField` that is automatically set to the current date and time when the question is created.

- **Methods:**
  - `__str__(self)`: Returns a string combining the quiz title and the question text.

### Answer
Represents an answer to a question.

- **Fields:**
  - `SINGLE_ANSWER`: A constant representing a single answer type.
  - `MULTIPLE_ANSWER`: A constant representing a multiple answer type.
  - `SELECT_WORD`: A constant representing a select word answer type.
  - `ANSWER_CHOICES`: A tuple of choices for the answer type.

## Imports

- `models`: The Django models module.
- `User`: The Django user model from `django.contrib.auth.models`.

## Usage

These models are used to create and manage the database tables for the quiz application. Below is an example of how to create a new quiz and add questions to it:

```python
from .models import Quiz, Question

# Create a new quiz
quiz = Quiz.objects.create(title="Sample Quiz", description="This is a sample quiz.")

# Add questions to the quiz
question1 = Question.objects.create(quiz=quiz, questions="What is the capital of France?")
question2 = Question.objects.create(quiz=quiz, questions="What is 2 + 2?")
