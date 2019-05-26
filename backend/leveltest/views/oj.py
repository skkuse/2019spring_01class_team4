import random
from django.db.models import Q, Count
from utils.api import APIView
from account.decorators import check_contest_permission
from ..models import LevelTestProblem
from ..serializers import LevelTestProblemSerializer


class LevelTestProblemAPI(APIView):

    def get(self, request):
        # 问题详情页
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = LevelTestProblem.objects.get(pk=problem_id)
                problem_data = LevelTestProblemSerializer(problem).data
                return self.success(problem_data)
            except LevelTestProblem.DoesNotExist:
                return self.error("Problem does not exist")

    

        problems = LevelTestProblem.objects.all()

        difficulty = request.GET.get("difficulty")
        if difficulty:
            problems = problems.filter(difficulty=difficulty)
        # 根据profile 为做过的题目添加标记
        data = self.paginate_data(request, problems, LevelTestProblemSerializer)
        return self.success(data)

