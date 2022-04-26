from rest_framework import serializers
from user.models import UserQuizSummary, UserQuizDetail

class UserQuizSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizSummary
        fields = '__all__'
    
class UserQuizDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizDetail
        fields = ('question_id','user_answer_id')

class CollaboratedSerializer(serializers.Serializer):
    summary = serializers.JSONField()
    detail = serializers.ListField()



