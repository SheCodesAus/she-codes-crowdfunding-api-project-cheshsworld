from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("projects/", views.ProjectList.as_view(),name="project-list"),
    path("projects/<int:pk>/", views.ProjectDetail.as_view()),
    path("projects/<int:pk>/comments/", views.ProjectCommentListApi.as_view()),
    path("pledges/", views.PledgeList.as_view(),name="pledge-list"),
    path("category/", views.CategoryList.as_view(), name="category-list"),
    path("category/<int:pk>/", views.CategoryDetailApi.as_view(), name="category-detail"),
    path("comment/", views.CommentListApi.as_view(), name="comment-list"),
    path("comment/<int:pk>/", views.CommentDetailApi.as_view(), name="comment-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
