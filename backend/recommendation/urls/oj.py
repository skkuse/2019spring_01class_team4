from django.conf.urls import url
from ..views.oj import ProvideRecommendationsAPI

urlpatterns = [
   # url(r"^problem/?$", ProblemAPI.as_view(), name="problem_api"),
    url(r"^recommendation/?$", ProvideRecommendationsAPI.as_view(), name="recommendation_api"),
]
