import random
from django.db.models import Q, Count
from utils.api import APIView
from account.decorators import check_contest_permission
from ..models import LevelTestProblem
from ..serializers import LevelTestProblemSerializer
from utils.api import APIView, CSRFExemptAPIView, validate_serializer, APIError
from account.models import User, UserProfile
from problem.models import QuriousDifficulty


int_from = {'low':0, 'mid':3, 'high':6}

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

        difficulty = request.GET.get("difficulty")
        problems = LevelTestProblem.objects.filter(difficulty=difficulty).order_by('ordering')

        data = self.paginate_data(request, problems, LevelTestProblemSerializer)
        return self.success(data)


    def post(self, request):
        data = request.data
        problem = LevelTestProblem.objects.create(**data)
        return self.success(problem.title)


class SubmitLevelTestAPI(APIView):

    def post(self, request):
        data = request.data
        difficulty = data['difficulty']
        correct = 0
        leveltest = LevelTestProblem.objects.filter(difficulty=difficulty).order_by('ordering')

        # 맞은 개수 채점
        for myanswer, problem in zip(data['answers'], leveltest):
            if problem.answer == int(myanswer):
                correct += 1
        
        # 난이도 고급의 경우 
        if difficulty == 'high':
            correct += sum([1 for a in data['answers'][3:] if a == 4])
            end = -1
            
        if correct == 1:
            return self.error('너무 어려우셨군요 ㅠㅠ 낮은 단계 혹은 추후에 다시 응시해주세요.')
        
        # 난이도 산정식
        level = ((correct + 2) // 3) + int_from[difficulty] + end
        qlevel = QuriousDifficulty.objects.get(pk=level)

        # 유저에게 실력수준 설정
        request.user.userprofile.level = qlevel
        print(request.user,':',level, request.user.userprofile.level.name)

        # 정답이 1개(10%미만)일 경우, 재시험을 요청한다.
        # 정답이 2~3개(10%이상 35%미만)일 경우, 중급1단계를 반환한다.
        # 정답이 4~6개(35%이상 60%미만)일 경우, 중급 2단계를 반환한다.
        # 정답이 7~9개(60% 이상 85% 미만)일 경우, 중급 3단계를 반환한다.
        # 정답이 10개~11개(85%)일 경우, 고급 1단계를 반환한다. 
        # 추후 진단고사 결과 반영한 실력수준 삽입
        # request.user.userprofile.hr_username = 'ddd'
        return self.success(qlevel.name)

