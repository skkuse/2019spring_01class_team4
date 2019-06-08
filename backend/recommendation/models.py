from django.db import models

from account.models import User
from problem.models import ProblemEX, Problem

# Create your models here.

# 추천 히스토리
# 1유저 - 1문제 추천 당 하나의 히스토리 생성
# 문제, 유저 외래키 생성
# round (int), is_Ex(boolean) created_at (datetime,생성될 때 자동으로 값 넣게끔), difficulty
class RecommendHistory(models.Model):
    round=models.IntegerField()
    is_Ex=models.BooleanField()
    created_at=models.DataTimeField(auto_now_add=True)
    difficulty=models.ForeignKey(Problem.QuriousDifficulty, null=True, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
