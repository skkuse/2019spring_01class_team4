import random
from django.db.models import Q, Count
from utils.api import APIView
from account.decorators import check_contest_permission
from ..models import LevelTestProblem
from ..serializers import LevelTestProblemSerializer
from utils.api import APIView, CSRFExemptAPIView, validate_serializer, APIError
from account.models import User, UserProfile

class LevelTestProblemAPI(APIView):

    def get(self, request):
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
            problems = problems.filter(difficulty=difficulty).order_by('ordering')

        data = self.paginate_data(request, problems, LevelTestProblemSerializer)
        return self.success(data)


    def post(self, request):
        data = request.data
        problem = LevelTestProblem.objects.create(**data)
        return self.success(problem.title)


class SubmitLevelTestAPI(APIView):

    def post(self, request):
        data = request.data
        correct = []
        leveltest = LevelTestProblem.objects.filter(difficulty=data['difficulty']).order_by('ordering')
        for myanswer, problem in zip(data['answers'], leveltest):
            if int(problem.answer) == int(myanswer):
                correct.push(True)
            else:
                correct.push(False)
        score = sum(correct)
        i=0
        while correct:
            if correct.pop(0):
                leveltest[i]
            i += 1
        # 추후 진단고사 결과 반영한 실력수준 삽입
        request.user.userprofile.hr_username = 'ddd'
        return self.success(score)

