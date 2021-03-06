import random
from django.db.models import Q, Count
from utils.api import APIView
from account.decorators import check_contest_permission
from ..models import ProblemTag, Problem, ProblemRuleType, ProblemEX
from ..serializers import ProblemSerializer, TagSerializer, ProblemSafeSerializer, ProblemEXSerializer
from contest.models import ContestRuleType
import requests
from bs4 import BeautifulSoup as bs
from recommendation.models import RecommendHistory



class ProblemTagAPI(APIView):
    def get(self, request):
        tags = ProblemTag.objects.annotate(problem_count=Count("problem")).filter(problem_count__gt=0)
        return self.success(TagSerializer(tags, many=True).data)


class PickOneAPI(APIView):
    def get(self, request):
        problems = Problem.objects.filter(contest_id__isnull=True, visible=True)
        count = problems.count()
        if count == 0:
            return self.error("No problem to pick")
        return self.success(problems[random.randint(0, count - 1)]._id)


class ProblemEXAPI(APIView):
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = ProblemEX.objects.get(pk=int(problem_id))
                problem_data = ProblemEXSerializer(problem).data
                return self.success(problem_data)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")

        problem = ProblemEX.objects.get(pk=request.GET.get('id',1))
        return self.success(ProblemEXSerializer(problem).data)



class SubmitProblemEXAPI(APIView):
    def get(self, request):
        problem = ProblemEX.objects.get(pk=request.GET.get('id',1))
        r = request.user.recommendhistory.filter(problemex=problem.id)[0]
        if r.is_Solved:
            return self.error("이미 풀이가 완료된 문제입니다.")
        # 테스트후에 이걸로
        # username = request.GET.get('username') 
        print(r.problemex.title)
        if problem.exbank == '백준':
            username = request.user.userprofile.bj_username
            soup = bs(requests.get('https://www.acmicpc.net/user/'+username).text,'html.parser')
            plist = [p.text for p in soup.select('div.panel-body')[0].select('span.problem_number')]
            if str(problem.pid) in plist:
                r.is_Solved = True
                r.save()
                return self.success('문제 풀이 완료')
            else:
                return self.error('문제를 풀지 않았습니다.')
        elif problem.exbank == '해커랭크':
            username = request.user.userprofile.hr_username
            print(username)
            response = requests.get('https://www.hackerrank.com/rest/hackers/'+username+'/recent_challenges?limit=10&cursor=&response_version=v2').json()
            print(response)
            for key in response['models']:
                if problem.url == 'https://www.hackerrank.com'+key['url']:
                    r.isSolved = True
                    r.save()
                    return self.success('문제 풀이 완료')
            return self.error('문제를 풀지 않았습니다.')


class ProblemAPI(APIView):
    @staticmethod
    def _add_problem_status(request, queryset_values):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            acm_problems_status = profile.acm_problems_status.get("problems", {})
            oi_problems_status = profile.oi_problems_status.get("problems", {})
            # paginate data
            results = queryset_values.get("results")
            if results is not None:
                problems = results
            else:
                problems = [queryset_values, ]
            for problem in problems:
                if problem["rule_type"] == ProblemRuleType.ACM:
                    problem["my_status"] = acm_problems_status.get(str(problem["id"]), {}).get("status")
                else:
                    problem["my_status"] = oi_problems_status.get(str(problem["id"]), {}).get("status")

    def get(self, request):
        # 问题详情页
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = Problem.objects.select_related("created_by") \
                    .get(_id=problem_id, contest_id__isnull=True, visible=True)
                problem_data = ProblemSerializer(problem).data
                self._add_problem_status(request, problem_data)
                return self.success(problem_data)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")

        limit = request.GET.get("limit")
        if not limit:
            return self.error("Limit is needed")

        problems = Problem.objects.select_related("created_by").filter(contest_id__isnull=True, visible=True)
        # 按照标签筛选
        tag_text = request.GET.get("tag")
        if tag_text:
            problems = problems.filter(tags__name=tag_text)

        # 搜索的情况
        keyword = request.GET.get("keyword", "").strip()
        if keyword:
            problems = problems.filter(Q(title__icontains=keyword) | Q(_id__icontains=keyword))


        difficulty = request.GET.get("difficulty")
        if difficulty:
            problems = problems.filter(difficulty=difficulty)
        # 根据profile 为做过的题目添加标记
        data = self.paginate_data(request, problems, ProblemSerializer)
        self._add_problem_status(request, data)
        return self.success(data)


class ContestProblemAPI(APIView):
    def _add_problem_status(self, request, queryset_values):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            if self.contest.rule_type == ContestRuleType.ACM:
                problems_status = profile.acm_problems_status.get("contest_problems", {})
            else:
                problems_status = profile.oi_problems_status.get("contest_problems", {})
            for problem in queryset_values:
                problem["my_status"] = problems_status.get(str(problem["id"]), {}).get("status")

    @check_contest_permission(check_type="problems")
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = Problem.objects.select_related("created_by").get(_id=problem_id,
                                                                           contest=self.contest,
                                                                           visible=True)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist.")
            if self.contest.problem_details_permission(request.user):
                problem_data = ProblemSerializer(problem).data
                self._add_problem_status(request, [problem_data, ])
            else:
                problem_data = ProblemSafeSerializer(problem).data
            return self.success(problem_data)

        contest_problems = Problem.objects.select_related("created_by").filter(contest=self.contest, visible=True)
        if self.contest.problem_details_permission(request.user):
            data = ProblemSerializer(contest_problems, many=True).data
            self._add_problem_status(request, data)
        else:
            data = ProblemSafeSerializer(contest_problems, many=True).data
        return self.success(data)
