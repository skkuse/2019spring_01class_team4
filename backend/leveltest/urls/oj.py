from django.conf.urls import url
from ..views.oj import LevelTestProblemAPI, SubmitLevelTestAPI

urlpatterns = [
   # url(r"^problem/?$", ProblemAPI.as_view(), name="problem_api"),
    url(r"^leveltest/?$", LevelTestProblemAPI.as_view(), name="leveltest_api"),
    url(r'^leveltest/submit/?$', SubmitLevelTestAPI.as_view(), name='leveltest_submit_api'),
]
