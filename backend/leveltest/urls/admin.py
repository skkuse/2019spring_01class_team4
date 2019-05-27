from django.conf.urls import url

from ..views.admin import LevelTestProblemAPI

urlpatterns = [
    # url(r"^test_case/?$", TestCaseAPI.as_view(), name="test_case_api"),
    url(r"^leveltest/?", LevelTestProblemAPI.as_view(), name="leveltest_problem_admin_api")
]
