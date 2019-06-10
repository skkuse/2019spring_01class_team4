import random
from django.db.models import Q, Count

from account.decorators import check_contest_permission
from utils.api import APIView, CSRFExemptAPIView, validate_serializer, APIError


from account.models import User, UserProfile

from problem.serializers import ProblemEXSerializer
from problem.models import ProblemEX, QuriousDifficulty
from ..models import RecommendHistory
from recommendation.serializers import RecommendHistorySerializer

class ProvideRecommendationsAPI(APIView):

    def get(self, request):
        u = User.objects.get(pk=1).userprofile
        problems = RecommendHistory.objects.filter(pk__in=u.current_reco)
        #data = self.paginate_data(request, problems, ProblemEXSerializer)
        data = self.paginate_data(request, problems, RecommendHistorySerializer)
        return self.success(data)



class CreateRecommendationsAPI(APIView):

    def get(self, request):
        # 사용자의 실력수준 가져오기
        # u_level = request.user.userprofile.level
        # QuriousDifficulty.problemex
        #problems = ProblemEX.objects.filter(exbank='백준')[:1]
        solved_p = [r for r in request.user.userprofile.current_reco if RecommendHistory.objects.get(pk=r).is_Solved]
        if len(solved_p) < 3:
            return self.error("추천해드리기에 푼 문제가 부족합니다. \n {}문제 더 풀어주세요.".format(3-len(solved_p)))
        
        problems = request.user.userprofile.level.problemex.all()

        u_level_id = request.user.userprofile.level.id 
        u_reco_round = request.user.userprofile.recommend_round
        u_current_reco = request.user.userprofile.current_reco
        # 사용자 실력수준내 내 기존 추천 문제 확인
        rhistory = request.user.recommendhistory.filter(difficulty=u_level_id)
        # 기존 외부 문제 추천 목록 추출
        phistory = [r.problemex for r in rhistory if r.is_Ex]
        # 추천하지 않았던 문제 리스트
        new_problems = [p for p in problems if p not in phistory]

        if len(new_problems) < 5:
            request.user.userprofile.level = QuriousDifficulty.objects.get(pk=u_level_id+1)
            request.user.userprofile.save()
            self.get(request)
        
        for np in new_problems[:5]:
            s = RecommendHistory.objects.create(round_num=u_reco_round+1, is_Ex=True, difficulty=request.user.userprofile.level, user=request.user, problemex=ProblemEX.objects.get(pk=np.id))  
            u_current_reco.append(s.id)

        for sp in solved_p:
            u_current_reco.pop(u_current_reco.index(sp))
        
        request.user.userprofile.current_reco = u_current_reco
        request.user.userprofile.recommend_round += 1
        request.user.userprofile.save()

        #data = self.paginate_data(request, u_current_reco, ProblemEXSerializer)
        return self.success(u_current_reco)

