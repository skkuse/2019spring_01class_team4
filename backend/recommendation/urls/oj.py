from django.conf.urls import url
from ..views.oj import ProvideRecommendationsAPI, CreateRecommendationsAPI

urlpatterns = [
   # url(r"^problem/?$", ProblemAPI.as_view(), name="problem_api"),
    url(r"^recommendation/?$", ProvideRecommendationsAPI.as_view(), name="recommendation_api"),
    url(r"^recommendation/create/?$", CreateRecommendationsAPI.as_view(), name="create_recommendation_api")
]
