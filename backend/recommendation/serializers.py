from rest_framework import serializers
from problem.models import ProblemEX
from problem.serializers import ProblemEXSerializer
from recommendation.models import RecommendHistory

class RecommendHistorySerializer(serializers.ModelSerializer):
    problemex = ProblemEXSerializer(read_only=True)

    class Meta:
        model = RecommendHistory
        fields = ('user','is_Ex','is_Solved','problemex')