"""
URL configuration for quizproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import QuizListAPIView,QuizDetailAPIView, SubmitQuizApiView,UserStatisticsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quizzes/', QuizListAPIView.as_view(), name='quiz-list'),
    path('quizzes/<int:quiz_id>/',QuizDetailAPIView.as_view(),name='quiz-detail'),
    path('quizzes/<int:quiz_id>/submit/',SubmitQuizApiView.as_view(),name='submit-quiz'),
    path('user-statistics/',UserStatisticsView.as_view(),name='user-statistics'), 
]
