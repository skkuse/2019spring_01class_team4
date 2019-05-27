import random
from django.db.models import Q, Count
from utils.api import APIView
from account.decorators import check_contest_permission
from ..models import LevelTestProblem
from ..serializers import LevelTestProblemSerializer
from utils.api import APIView, CSRFExemptAPIView, validate_serializer, APIError

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


