from .models import LevelTestProblem
from rest_framework import serializers


class LevelTestProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTestProblem
        exclude = ('answer',)
        

class CreateLevelTestProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTestProblem
        fields = '__all__'
        