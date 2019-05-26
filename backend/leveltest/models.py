from django.db import models

from utils.models import JSONField
from utils.models import RichTextField


class LevelTestProblem(models.Model):

    title = models.TextField()
    description = RichTextField()
    answer = models.IntegerField() # 1~5 숫자중 하나
    choices = JSONField() # key: 1~5 / value: 선택지
    ordering = models.IntegerField()
    difficulty = models.TextField()

    class Meta:
        db_table = 'level_test_problem'
