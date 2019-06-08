import random
from django.db.models import Q, Count

from account.decorators import check_contest_permission
from utils.api import APIView, CSRFExemptAPIView, validate_serializer, APIError


from account.models import User, UserProfile

from problem.serializers import ProblemEXSerializer
from problem.models import ProblemEX, QuriousDifficulty



class ProvideRecommendationsAPI(APIView):

    def get(self, request):
        # 사용자의 실력수준 가져오기
        # u_level = request.user.userprofile.level
        # QuriousDifficulty.problemex
        #problems = ProblemEX.objects.filter(exbank='백준')[:1]
        problems = ProblemEX.objects.filter(exbank='해커랭크')[:3]

        data = self.paginate_data(request, problems, ProblemEXSerializer)
        return self.success(data)

