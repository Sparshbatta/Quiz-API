from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import UserQuizSummary, UserQuizDetail
from quiz.models import Question, Options
from .serializers import CollaboratedSerializer, UserQuizDetailSerializer, UserQuizSummarySerializer


@api_view(['GET','POST'])
def userQuizSummaryView(request):
    summary = UserQuizSummary.objects.all()
    serializer = UserQuizSummarySerializer(summary,many=True)

    return Response({'summary':serializer.data})


@api_view(['GET','POST'])
def userQuizDetailView(request):
    detail = UserQuizDetail.objects.all()
    serializer = UserQuizDetailSerializer(detail,many=True)
    return Response({'detail':serializer.data})




@api_view(['POST'])
def createUserQuizView(request):
    serializer = UserQuizSummarySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def createUserDetailView(request):
    serializer = UserQuizDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateUserDetailView(request,pk):
    detail = UserQuizDetail.objects.get(id=pk)
    serializer = UserQuizDetailSerializer(instance= detail, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateUserSummaryView(request,pk):
    summary = UserQuizSummary.objects.get(id=pk)
    serializer = UserQuizSummarySerializer(instance = summary, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



#final answer may vary from original assignment as some new custom objects corresponding to Question
#models have been added into the Questions model class having random weights

#main working function 

@api_view(['POST'])
def collaborateView(request):
    serializer = CollaboratedSerializer(request.data)
    quiz_name = serializer.data['summary']['quiz_name']
    quiz_date = serializer.data['summary']['quiz_date']
    user = serializer.data['summary']['user']
    summary = UserQuizSummary.objects.create(quiz_name=quiz_name,quiz_date=quiz_date,user=user,no_correct_attempt=0,no_wrong_attempt=0)
    summary.save()
    num_correct = 0
    num_wrong = 0
    weight = 0

    for i in serializer.data['detail']:
        question_id = i['question_id']
        question = Question.objects.get(id=question_id)
        user_answer_id = i['user_answer_id']
        option = Options.objects.get(id=user_answer_id)
        num_correct += option.option_flag
        if option.option_text=='Yes':
            weight += question.weight
        elif option.option_text=='Partially Completed':
            weight+= question.weight/2
        num_wrong += not (option.option_flag)

        #partially correct would also be considered as wrong but the weight would be added accordingly

        detail = UserQuizDetail.objects.create(quiz_id=summary,question_id=question,user_answer_id=user_answer_id)
        detail.save()
    summary.no_correct_attempt = num_correct
    summary.no_wrong_attempt = num_wrong
    summary.save()
    return Response({'num_correct':num_correct,'num_wrong':num_wrong,'score_percentage':weight})